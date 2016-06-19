# -*- coding: utf-8 -*-

import html2text
def html2md(text):
    h = html2text.HTML2Text()
    h.mark_code = True
    if isinstance(text, unicode):
        return h.handle(text).encode("UTF-8")
    # FIXME: convert to unicode in case it isn't?
