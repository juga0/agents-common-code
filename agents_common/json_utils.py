# -*- coding: utf-8 -*-

import json
import logging

logger = logging.getLogger(__name__)


def read_json(path):
    with open(path) as f:
        obj = json.load(f)
    return obj


def write_json(obj, filepath):
    if obj:
        with open(filepath, 'w') as f:
            json.dump(obj, f, indent=2)
