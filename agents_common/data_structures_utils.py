# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger(__name__)


def merge_two_dicts(x, y):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    z = x.copy()
    z.update(y)
    return z


def get_value_from_key_index(dict_or_list, keys_indexes):
    """"""
    if isinstance(keys_indexes, list):
        for k in keys_indexes:
            logger.debug('key %s', k)
            try:
                print('dict_or_list %s', dict_or_list)
                print('k %s', k)
                dict_or_list = dict_or_list[k]
            except (KeyError, IndexError) as e:
                logger.error(e)
                return dict_or_list
        return dict_or_list
    return dict_or_list.get(keys_indexes)
