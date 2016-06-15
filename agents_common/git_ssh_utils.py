# -*- coding: utf-8 -*-

from os import environ, makedirs, chmod
from os.path import isdir, isfile
import logging

logger = logging.getLogger(__name__)


def check_ssh_keys(repo, git_ssh_command_path, ssh_priv_key_path,
                   ssh_pub_key_path, ssh_pub_key_path_server):

        with open(ssh_pub_key_path, 'r') as f:
            logger.debug('ssh pub key %s' % f.read())
        with open(ssh_priv_key_path, 'r') as f:
            logger.debug('ssh priv key %s' % f.read())
        with open(ssh_pub_key_path_server, 'r') as f:
            logger.debug('ssh pub key server %s' % f.read())
        origin = repo.remotes[0]
        logger.debug('pushing with git_ssh_command_path %s' %
                     git_ssh_command_path)
        # more debugging for morph.io
        with open(git_ssh_command_path) as f:
            logger.debug('ssh command content %s' % f.read())
        logger.debug('MORPH_SSH_PUB_KEY')
        logger.debug(environ.get('MORPH_SSH_PUB_KEY'))
        logger.debug('MORPH_SSH_PRIV_KEY')
        logger.debug(environ.get('MORPH_SSH_PRIV_KEY'))
        with repo.git.custom_environment(GIT_SSH=git_ssh_command_path):
            logger.debug('GIT_SSH %s' % environ.get('GIT_SSH'))
            logger.debug('GIT_SSH_COMMAND %s' % environ.get('GIT_SSH_COMMAND'))
        with origin.repo.git.custom_environment(GIT_SSH=git_ssh_command_path):
            logger.debug('GIT_SSH %s' % environ.get('GIT_SSH'))
            logger.debug('GIT_SSH_COMMAND %s' % environ.get('GIT_SSH_COMMAND'))
        environ['GIT_SSH'] = git_ssh_command_path
        logger.debug('GIT_SSH %s' % environ.get('GIT_SSH'))


def write_ssh_keys(ssh_dir, ssh_priv_key_env, ssh_pub_key_env,
                   ssh_priv_key_path, ssh_pub_key_path):
    ssh_pub_key = environ[ssh_pub_key_env]
    ssh_priv_key = environ[ssh_priv_key_env]
    logger.debug('ssh_dir %s' % ssh_dir)
    if not isdir(ssh_dir):
        makedirs(ssh_dir)
        logger.debug('created dir %s' % ssh_dir)
    if not isfile(ssh_pub_key_path):
        with open(ssh_pub_key_path, 'wb') as f:
            f.write(ssh_pub_key)
        logger.debug('wroten %s' % ssh_pub_key_path)
    if not isfile(ssh_priv_key_path):
        with open(ssh_priv_key_path, 'wb') as f:
            f.write(ssh_priv_key)
        logger.debug('wroten %s' % ssh_priv_key_path)
        chmod(ssh_priv_key_path, 0600)


def write_ssh_command(git_ssh_command_path, git_ssh_command):
    if not isfile(git_ssh_command_path):
        with open(git_ssh_command_path, 'w') as f:
            f.write(git_ssh_command)
        chmod(git_ssh_command_path, 0766)
        logger.debug('wroten %s' % git_ssh_command_path)
        logger.debug('with content %s' % git_ssh_command)


def write_ssh_key_server(ssh_pub_key, ssh_pub_key_path):
    if not isfile(ssh_pub_key_path):
        with open(ssh_pub_key_path, 'w') as f:
            f.write(ssh_pub_key)
        logger.debug('wroten %s' % ssh_pub_key_path)
        logger.debug('with content %s' % ssh_pub_key)
