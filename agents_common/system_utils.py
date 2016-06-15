# -*- coding: utf-8 -*-

from os import environ
import logging

logger = logging.getLogger(__name__)


# def obtain_python_version():
#     import sys
#     python_version = sys.version
#     logger.debug(python_version)


def obtain_uname():
    from os import uname
    kernel_version = ' '.join(uname())
    logger.debug(kernel_version)
    return kernel_version


# def obtain_system_hostname():
#     import socket
#     s = socket.socket()
#     host = socket.gethostname()
#     logger.debug(host)


# def obtain_user():
#     import getpass
#     getpass.getuser()


def obtain_home():
    from os.path import expanduser
    home = expanduser('~')
    logger.debug('home %s' % home)
    return home


def obtain_environ():
    from os import environ
    logger.debug('environ %s' % environ)
    return environ


def ls(dir_path):
    from os import listdir
    ls = listdir(dir_path)
    logger.debug('ls %s' % ls)
    return ls



def obtain_ip():
    import socket
    ip = socket.gethostbyname(socket.gethostname())
    logger.debug('ip %s' % ip)
    return ip


def obtain_public_ip():
    from urllib2 import urlopen
    my_ip = urlopen('http://ip.42.pl/raw').read()
    logger.debug('public ip %s' % my_ip)
    return str(my_ip)


def hasproxy():
    # FIXME: http proxy might not change the public address,
    # assuming it does for now
    if environ.get('HTTP_PROXY'):
        logger.debug('there is an HTTP_PROXY')
        return True
    logger.debug('there is not an HTTP_PROXY')
    return False



def now():
    from datetime import datetime
    now = datetime.now()
    logger.debug(now)
    return now
