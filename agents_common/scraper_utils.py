# -*- coding: utf-8 -*-

import os.path
from datetime import datetime
import logging
import lxml.html
import lxml.etree

utf8_parser = lxml.etree.XMLParser(encoding='utf-8')
logger = logging.getLogger(__name__)


def last_modified2timestamp_str(last_modified):
    """
    Returns the current last_modified header of a Web page
    (Mon, 13 Jun 2016 19:01:36 GMT) in ISO 8601 (yyyy-MM-ddTHH:mm:ssZ) date
    time without dashes (yyyyMMddTHHmmssZ).
    >>> last_modified = 'Mon, 13 Jun 2016 19:01:36 GMT'
    >>> last_modified2timestamp_str(last_modified)
    '20160613T190136Z'
    Also:
    iso8601.parse_date(datetime.datetime.now(tz=pytz.utc).isoformat())
    """
    dt = datetime.strptime(last_modified, '%a, %d %b %Y %H:%M:%S %Z')
    from pytz import timezone
    dt.replace(tzinfo=timezone(last_modified.split()[-1:][0]))
    return dt.isoformat().replace(':', '').replace('-', '') + 'Z'


def now_timestamp_str_nodashes():
    """
    Return the current date time in ISO 8601 (yyyy-MM-ddTHH:mm:ssZ)
    without dashes ((yyyyMMddTHHmmssZ)).
    >> import datetime
    >> datetime.utcnow().replace(microsecond=0).isoformat().replace(':', '')\
         .replace('-', '') + 'Z'
    """
    return datetime.now().replace(microsecond=0).isoformat().replace(':', '')\
        .replace('-', '') + 'Z'


def now_timestamp_ISO_8601():
    """
    # assuming that utcnow returns the correct local time converted to UTC:
    >> datetime.utcnow().isoformat()
    '2016-07-30T13:36:06.305653'
    # for python timezone aware objects:
    >> datetime.now(tz=pytz.utc).isoformat()
    '2016-07-30T13:37:23.748609+00:00'
    Both 'Z' and '+00:00' are compatible with iso format
    """
    return datetime.utcnow().isoformat() + 'Z'

def now_timestamp():
    return datetime.utcnow().replace(microsecond=0).isoformat()\
        .replace(':', '-') + 'Z'


def rm_disallowd_chars(filename):
    import string
    import unicodedata
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    valid_filename = unicodedata.normalize('NFKD', filename)\
        .encode('ASCII', 'ignore')
    return ''.join(c for c in valid_filename if c in valid_chars)


def url2filenamedashes(url):
    """
    Convert a url (https://staging-store.openintegrity.org/url) into a POSIX
    file name ()

    >>> url = 'https://staging-store.openintegrity.org/url'
    >>> url.replace(' ', '_').replace('://', '-').replace('/', '-')
    'https-staging-store.openintegrity.org-url'
    """
    # return url.replace(' ', '_').replace('://', '-').replace('/', '-')
    return rm_disallowd_chars(unicode(url))


def url2filename(text):
    return text.replace(' ', '_').replace('https://', '')\
        .replace('http://', '').replace('/', '_')


def append(file, string):
    file = open(file, 'a')
    file.write(string + "\n")
    file.close()


def save_html(body, path, args):
    logger.debug(args)
    html_path = (path % args)[:255]
    if not os.path.isdir(path):
        os.makedirs(path)
    with open(html_path,  'w') as f:
        f.write(body)
    logger.debug('saving html %s' % html_path)


# needed?
def parse_from_unicode(unicode_str):
    # FIXME: not needed?
    if isinstance(unicode_str, unicode):
        s = unicode_str.encode('utf-8')
        return lxml.etree.fromstring(s, parser=utf8_parser)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
