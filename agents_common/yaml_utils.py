# -*- coding: utf-8 -*-

import sys
import yaml
import logging

logger = logging.getLogger(__name__)


def read_yaml(file_path, exit_on_error=False):
    try:
        with open(file_path) as f:
            yaml_data = yaml.safe_load(f)
        logger.debug('yaml data: ')
        logger.debug(yaml_data)
        return yaml_data
    except IOError as e:
        logger.exception(e)
        logger.debug('cant obtain yaml file')
        if exit_on_error:
            sys.exit()
        raise IOError


def generate_yaml(obj):
    data_yaml = yaml.safe_dump(obj)
    logger.debug(data_yaml)
    return data_yaml


def write_yaml(obj, filepath):
    if obj:
        with open(filepath, 'w') as f:
            f.write(yaml.safe_dump(obj))
