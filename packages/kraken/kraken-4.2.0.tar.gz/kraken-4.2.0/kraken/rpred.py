#
# Copyright 2015 Benjamin Kiessling
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing
# permissions and limitations under the License.
"""
kraken.rpred
~~~~~~~~~~~~

Generators for recognition on lines images.
"""
import logging
import bidi.algorithm as bd

from PIL import Image
from functools import partial
from collections import defaultdict
from typing import List, Tuple, Optional, Generator, Union, Dict, Sequence

from kraken.lib.util import get_im_str, is_bitonal
from kraken.lib.models import TorchSeqRecognizer
from kraken.lib.segmentation import extract_polygons, compute_polygon_section
from kraken.lib.exceptions import KrakenInputException
from kraken.lib.dataset import ImageInputTransforms

import copy

__all__ = ['ocr_record', 'bidi_record', 'mm_rpred', 'rpred']

logger = logging.getLogger(__name__)


class ocr_record(object):
    """
    A record object containing the recognition result of a single line
    """
    def __init__(self, prediction: str, cuts, confidences: List[float], line: Union[List, Dict[str, List]]) -> None:
        self.prediction = prediction
        self.cuts = cuts
        self.confidences = confidences
        self.tags = None if 'tags' not in line else line['tags']
        self.type = 'baselines' if 'baseline' in line else 'box'
        self.base_dir = None
        if self.type == 'baselines':
            self.line = line['boundary']
            self.baseline = line['baseline']
        else:
            self.line = line

    def __len__(self) -> int:
        return len(self.prediction)

    def __str__(self) -> str:
        return self.prediction

    def __iter__(self):
        self.idx = -1
        return self

    def __next__(self) -> Tuple[str, int, float]:
        if self.idx + 1 < len(self):
            self.idx += 1
            return (self.prediction[self.idx], self.cuts[self.idx],
                    self.confidences[self.idx])
        else:
            raise StopIteration

    def __getitem__(self, key: Union[int, slice]):
        if isinstance(key, slice):
            return [self[i] for i in range(*key.indices(len(self)))]
        elif isinstance(key, int):
            if key < 0:
                key += len(self)
            if key >= len(self):
                raise IndexError('Index (%d) is out of range' % key)
            return (self.prediction[key], self.cuts[key],
                    self.confidences[key])
        else:
            raise TypeError('Invalid argument type')


def bidi_record(record: ocr_record, base_dir=None) -> ocr_record:
    """
    Reorders a record using the Unicode BiDi algorithm.

    Models trained for RTL or mixed scripts still emit classes in LTR order
    requiring reordering for proper display.

    Args:
        record (kraken.rpred.ocr_record)

    Returns:
        kraken.rpred.ocr_record
    """
    storage = bd.get_empty_storage()

    if base_dir not in ('L', 'R'):
        base_level = bd.get_base_level(record.prediction)
    else:
        base_level = {'L': 0, 'R': 1}[base_dir]

    storage['base_level'] = base_level
    storage['base_dir'] = ('L', 'R')[base_level]

    bd.get_embedding_levels(record.prediction, storage)
    bd.explicit_embed_and_overrides(storage)
    bd.resolve_weak_types(storage)
    bd.resolve_neutral_types(storage, False)
    bd.resolve_implicit_levels(storage, False)
    for i, j in enumerate(record):
        storage['chars'][i]['record'] = j
    bd.reorder_resolved_levels(storage, False)
    bd.apply_mirroring(storage, False)
    prediction = ''
    cuts = []
    confidences = []
    for ch in storage['chars']:
        # code point may have been mirrored
        prediction = prediction + ch['ch']
        cuts.append(ch['record'][1])
        confidences.append(ch['record'][2])
    # carry over whole line information
    if record.type == 'baselines':
        line = {'boundary': record.line, 'baseline': record.baseline}
    else:
        line = record.line
    rec = ocr_record(prediction, cuts, confidences, line)
    rec.tags = record.tags
    rec.base_dir = base_dir
    return rec


class mm_rpred(object):
    """
    Multi-model version of kraken.rpred.rpred
    """
    def __init__(self,
                 nets: Dict[str, TorchSeqRecognizer],
                 im: Image.Image,
                 bounds: dict,
                 pad: int = 16,
                 bidi_reordering: Union[bool, str] = True,
                 tags_ignore: Optional[List[str]] = None) -> Generator[ocr_record, None, None]:
        """
        Multi-model version of kraken.rpred.rpred.

        Takes a dictionary of ISO15924 script identifiers->models and an
        script-annotated segmentation to dynamically select appropriate models for
        these lines.

        Args:
            nets (dict): A dict mapping tag values to TorchSegRecognizer
                         objects. Recommended to be an defaultdict.
            im (PIL.Image.Image): Image to extract text from
            bounds (dict): A dictionary containing a 'boxes' entry
                            with a list of lists of coordinates (script, (x0, y0,
                            x1, y1)) of a text line in the image and an entry
                            'text_direction' containing
                            'horizontal-lr/rl/vertical-lr/rl'.
            pad (int): Extra blank padding to the left and right of text line
            bidi_reordering (bool|str): Reorder classes in the ocr_record according to
                                        the Unicode bidirectional algorithm for
                                        correct display. Set to L|R to
                                        override default text direction.
            tags_ignore (list): List of tag values to ignore during recognition
        Yields:
            An ocr_record containing the recognized text, absolute character
            positions, and confidence values for each character.

        Raises:
            KrakenInputException if the mapping between segmentation tags and
            networks is incomplete.
        """
        seg_types = set(recognizer.seg_type for recognizer in nets.values())
        if isinstance(nets, defaultdict):
            seg_types.add(nets.default_factory().seg_type)
            self._resolve_tags_to_model = partial(_resolve_tags_to_model, default=nets.default_factory())
        else:
            self._resolve_tags_to_model = _resolve_tags_to_model

        if not tags_ignore:
            tags_ignore = []

        if ('type' in bounds and bounds['type'] not in seg_types) or len(seg_types) > 1:
            logger.warning(f'Recognizers with segmentation types {seg_types} will be '
                           f'applied to segmentation of type {bounds["type"] if "type" in bounds else None}. '
                           f'This will likely result in severely degraded performace')
        one_channel_modes = set(recognizer.nn.one_channel_mode for recognizer in nets.values())
        if '1' in one_channel_modes and len(one_channel_modes) > 1:
            raise KrakenInputException('Mixing binary and non-binary recognition models is not supported.')
        elif '1' in one_channel_modes and not is_bitonal(im):
            logger.warning('Running binary models on non-binary input image '
                           '(mode {}). This will result in severely degraded '
                           'performance'.format(im.mode))
        if 'type' in bounds and bounds['type'] == 'baselines':
            valid_norm = False
            self.len = len(bounds['lines'])
            self.seg_key = 'lines'
            self.next_iter = self._recognize_baseline_line
            self.line_iter = iter(bounds['lines'])
            tags = set()
            for x in bounds['lines']:
                tags.update(x['tags'].values())
        else:
            valid_norm = True
            self.len = len(bounds['boxes'])
            self.seg_key = 'boxes'
            self.next_iter = self._recognize_box_line
            self.line_iter = iter(bounds['boxes'])
            tags = set(x[0] for line in bounds['boxes'] for x in line)

        im_str = get_im_str(im)
        logger.info('Running {} multi-script recognizers on {} with {} lines'.format(len(nets), im_str, self.len))

        filtered_tags = []
        miss = []
        for tag in tags:
            if not isinstance(nets, defaultdict) and (not nets.get(tag) and tag not in tags_ignore):
                miss.append(tag)
            elif tag not in tags_ignore:
                filtered_tags.append(tag)
        tags = filtered_tags

        if miss:
            raise KrakenInputException('Missing models for tags {}'.format(set(miss)))

        # build dictionary for line preprocessing
        self.ts = {}
        for tag in tags:
            logger.debug('Loading line transforms for {}'.format(tag))
            network = nets[tag]
            batch, channels, height, width = network.nn.input
            self.ts[tag] = ImageInputTransforms(batch, height, width, channels, pad, valid_norm)

        self.im = im
        self.nets = nets
        self.bidi_reordering = bidi_reordering
        self.pad = pad
        self.bounds = bounds
        self.tags_ignore = tags_ignore

    def _recognize_box_line(self, line):
        flat_box = [point for box in line['boxes'][0] for point in box[1]]
        xmin, xmax = min(flat_box[::2]), max(flat_box[::2])
        ymin, ymax = min(flat_box[1::2]), max(flat_box[1::2])
        rec = ocr_record('', [], [], [[xmin, ymin], [xmin, ymax], [xmax, ymax], [xmax, ymin]])
        for tag, (box, coords) in zip(map(lambda x: x[0], line['boxes'][0]),
                                      extract_polygons(self.im, {'text_direction': line['text_direction'],
                                                                 'boxes': map(lambda x: x[1], line['boxes'][0])})):
            self.box = box
            # skip if tag is set to ignore
            if self.tags_ignore is not None and tag in self.tags_ignore:
                logger.warning(f'Ignoring {tag} line segment.')
                continue
            # check if boxes are non-zero in any dimension
            if 0 in box.size:
                logger.warning(f'bbox {coords} with zero dimension. Emitting empty record.')
                continue
            # try conversion into tensor
            try:
                logger.debug('Preparing run.')
                line = self.ts[tag](box)
            except Exception:
                logger.warning(f'Conversion of line {coords} failed. Skipping.')
                continue

            # check if line is non-zero
            if line.max() == line.min():
                logger.warning('Empty run. Skipping.')
                continue

            _, net = self._resolve_tags_to_model({'type': tag}, self.nets)

            logger.debug(f'Forward pass with model {tag}.')
            preds = net.predict(line.unsqueeze(0))[0]

            # calculate recognized LSTM locations of characters
            logger.debug('Convert to absolute coordinates')
            # calculate recognized LSTM locations of characters
            # scale between network output and network input
            self.net_scale = line.shape[2]/net.outputs.shape[2]
            # scale between network input and original line
            self.in_scale = box.size[0]/(line.shape[2]-2*self.pad)

            pred = ''.join(x[0] for x in preds)
            pos = []
            conf = []

            for _, start, end, c in preds:
                if self.bounds['text_direction'].startswith('horizontal'):
                    xmin = coords[0] + self._scale_val(start, 0, self.box.size[0])
                    xmax = coords[0] + self._scale_val(end, 0, self.box.size[0])
                    pos.append([[xmin, coords[1]], [xmin, coords[3]], [xmax, coords[3]], [xmax, coords[1]]])
                else:
                    ymin = coords[1] + self._scale_val(start, 0, self.box.size[1])
                    ymax = coords[1] + self._scale_val(end, 0, self.box.size[1])
                    pos.append([[coords[0], ymin], [coords[2], ymin], [coords[2], ymax], [coords[0], ymax]])
                conf.append(c)
            rec.prediction += pred
            rec.cuts.extend(pos)
            rec.confidences.extend(conf)
        if self.bidi_reordering:
            logger.debug('BiDi reordering record.')
            return bidi_record(rec, base_dir=self.bidi_reordering if self.bidi_reordering in ('L', 'R') else None)
        else:
            logger.debug('Emitting raw record')
            return rec

    def _recognize_baseline_line(self, line):
        if self.tags_ignore is not None:
            for tag in line['lines'][0]['tags'].values():
                if tag in self.tags_ignore:
                    logger.info(f'Ignoring line segment with tags {line["lines"][0]["tags"]} based on {tag}.')
                    return ocr_record('', [], [], line['lines'][0])

        try:
            box, coords = next(extract_polygons(self.im, line))
        except KrakenInputException as e:
            logger.warning(f'Extracting line failed: {e}')
            return ocr_record('', [], [], line['lines'][0])

        self.box = box

        tag, net = self._resolve_tags_to_model(coords['tags'], self.nets)
        # check if boxes are non-zero in any dimension
        if 0 in box.size:
            logger.warning(f'bbox {coords} with zero dimension. Emitting empty record.')
            return ocr_record('', [], [], coords)
        # try conversion into tensor
        try:
            line = self.ts[tag](box)
        except Exception:
            return ocr_record('', [], [], coords)
        # check if line is non-zero
        if line.max() == line.min():
            return ocr_record('', [], [], coords)

        preds = net.predict(line.unsqueeze(0))[0]
        # calculate recognized LSTM locations of characters
        # scale between network output and network input
        self.net_scale = line.shape[2]/net.outputs.shape[2]
        # scale between network input and original line
        self.in_scale = box.size[0]/(line.shape[2]-2*self.pad)

        # XXX: fix bounding box calculation ocr_record for multi-codepoint labels.
        pred = ''.join(x[0] for x in preds)
        pos = []
        conf = []
        for _, start, end, c in preds:
            pos.append(compute_polygon_section(coords['baseline'],
                                               coords['boundary'],
                                               self._scale_val(start, 0, self.box.size[0]),
                                               self._scale_val(end, 0, self.box.size[0])))
            conf.append(c)
        if self.bidi_reordering:
            logger.debug('BiDi reordering record.')
            return bidi_record(ocr_record(pred, pos, conf, coords),
                               base_dir=self.bidi_reordering if self.bidi_reordering in ('L', 'R') else None)
        else:
            logger.debug('Emitting raw record')
            return ocr_record(pred, pos, conf, coords)

    def __next__(self):
        bound = self.bounds
        bound[self.seg_key] = [next(self.line_iter)]
        return self.next_iter(bound)

    def __iter__(self):
        return self

    def __len__(self):
        return self.len

    def _scale_val(self, val, min_val, max_val):
        return int(round(min(max(((val*self.net_scale)-self.pad)*self.in_scale, min_val), max_val-1)))


def rpred(network: TorchSeqRecognizer,
          im: Image.Image,
          bounds: dict,
          pad: int = 16,
          bidi_reordering: Union[bool, str] = True) -> Generator[ocr_record, None, None]:
    """
    Uses a TorchSeqRecognizer and a segmentation to recognize text

    Args:
        network (kraken.lib.models.TorchSeqRecognizer): A TorchSegRecognizer
                                                        object
        im (PIL.Image.Image): Image to extract text from
        bounds (dict): A dictionary containing a 'boxes' entry with a list of
                       coordinates (x0, y0, x1, y1) of a text line in the image
                       and an entry 'text_direction' containing
                       'horizontal-lr/rl/vertical-lr/rl'.
        pad (int): Extra blank padding to the left and right of text line.
                   Auto-disabled when expected network inputs are incompatible
                   with padding.
        bidi_reordering (bool|str): Reorder classes in the ocr_record according to
                                    the Unicode bidirectional algorithm for correct
                                    display. Set to L|R to change base text
                                    direction.
    Yields:
        An ocr_record containing the recognized text, absolute character
        positions, and confidence values for each character.
    """
    bounds = copy.deepcopy(bounds)
    if 'boxes' in bounds:
        boxes = bounds['boxes']
        rewrite_boxes = []
        for box in boxes:
            rewrite_boxes.append([('default', box)])
        bounds['boxes'] = rewrite_boxes
        bounds['script_detection'] = True
    return mm_rpred(defaultdict(lambda: network), im, bounds, pad, bidi_reordering)


def _resolve_tags_to_model(tags: Sequence[Dict[str, str]],
                           model_map: Dict[str, TorchSeqRecognizer],
                           default: Optional[TorchSeqRecognizer] = None) -> TorchSeqRecognizer:
    """
    Resolves a sequence of tags
    """
    for tag in tags.values():
        if tag in model_map:
            return tag, model_map[tag]
    if default:
        return next(tags.values()), default
    raise KrakenInputException('No model for tags {}'.format(tags))
