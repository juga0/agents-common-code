"""Conditional HTTP GET using ETag header
(based on http://www.artima.com/forums/flat.jsp?forum=122&thread=15024)."""

import requests
import logging

# logger.basicConfig()
logger = logging.getLogger(__name__)
# logger.setLevel(logger.DEBUG)


def get_etag(url):
    r = requests.head(url)
    headers = r.headers
    # logger.debug('response headers %s', headers)
    etag = headers.get('ETag')
    logger.debug('header response etag: %s', etag)
    last_modified = headers.get("Last-Modified")
    logger.debug('header response last-modifed: %s', last_modified)
    if not etag and not last_modified:
        logger.debug('url %s does not return etag nor last_modified', url)
    return etag, last_modified

def get_ismodified(url, etag=None, last_modified=None):
    headers = {}
    if etag:
        headers["If-None-Match"] = etag
        logger.debug('request with header etag %s' % etag)
    elif last_modified:
        headers["If-Modified-Since"] = last_modified
        logger.debug('request with header last-modifed %s' % last_modified)
    logger.debug('request headers %s', headers)
    r = requests.get(url, headers=headers)
    if r.status_code == 304 and (etag or last_modified):
        logger.info("the web page has not been modified")
        return False, r
        # data = url_handle.read()
    logging.info('the web page has been modified')
    return True, r


# url = 'http://apache.org/'
# etag, last_modified = get_etag(url)
# ismodified, url_handle = get_ismodified(url, etag, last_modified)
# print ismodified
