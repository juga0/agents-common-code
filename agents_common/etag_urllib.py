"""Conditional HTTP GET using ETag header
(based on http://www.artima.com/forums/flat.jsp?forum=122&thread=15024)."""

import urllib2
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class NotModifiedHandler(urllib2.BaseHandler):
    def http_error_304(self, req, fp, code, message, headers):
        addinfourl = urllib2.addinfourl(fp, headers, req.get_full_url())
        addinfourl.code = code
        return addinfourl


def get_etag(url):
    req = urllib2.Request(URL)
    url_handle = urllib2.urlopen(req)
    headers = url_handle.info()
    logger.debug('response headers %s', headers)
    etag = headers.getheader("ETag")
    logging.debug('header response etag: %s', etag)
    last_modified = headers.getheader("Last-Modified")
    logging.debug('header response last-modifed: %s', last_modified)
    return etag, last_modified


def get_ismodified(url, etag=None, last_modified=None):
    req = urllib2.Request(URL)
    if etag:
        req.add_header("If-None-Match", etag)
        logger.debug('request with header etag %s' % etag)
    elif last_modified:
        req.add_header("If-Modified-Since", last_modified)
        logger.debug('request with header last-modifed %s' % last_modified)
    logger.debug('request headers %s', req.headers)
    opener = urllib2.build_opener(NotModifiedHandler())
    url_handle = opener.open(req)
    headers = url_handle.info()
    if hasattr(url_handle, 'code') and url_handle.code == 304 \
            and (etag or last_modified):
        logging.info("the web page has not been modified")
        return False, url_handle
    # data = url_handle.read()d['Last-Modified'] = 'Tue, 14 Jun 2016 00:10:22 GMT'
d['ETag'] = '"d266-53531d4b9a870"'
kwargs = {'headers': d}
r = requests.head(url, **kwargs)

    return True, url_handle

url = 'http://python.org/'
etag, last_modified = get_etag(url)
ismodified, url_handle = get_ismodified(url, etag, last_modified)
print ismodified


# d['Last-Modified'] = 'Tue, 14 Jun 2016 00:10:22 GMT'
# d['ETag'] = '"d266-53531d4b9a870"'
# kwargs = {'headers': d}
# r = requests.head(url, **kwargs)
