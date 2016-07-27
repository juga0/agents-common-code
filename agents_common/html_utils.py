# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger(__name__)

import html2text
def html2md(text, encoding='utf-8'):
    logger.debug('converting to markdown')
    logger.debug('type text %s', type(text))
    h = html2text.HTML2Text()
    h.mark_code = True
    if isinstance(text, unicode):
        return h.handle(text).encode(encoding)
    return h.handle(text)
