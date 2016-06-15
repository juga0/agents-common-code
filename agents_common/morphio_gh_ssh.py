# -*- coding: utf-8 -*-

from os import environ

from morphio_config import SSH_DIR, SSH_PRIV_KEY_PATH, SSH_PUB_KEY_PATH, \
    MORPH_SSH_PUB_KEY_ENV, MORPH_SSH_PRIV_KEY_ENV
    GIT_SSH_COMMAND_PATH, GIT_SSH_COMMAND_MORPHIO, \
    SSH_PUB_KEY_SERVER, SSH_PUB_KEY_SERVER_PATH, \
    DATA_REPO_PATH, DATA_REPO_BRANCH
from git_ssh_utils import pull_or_clone
import logging

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)

DATA_REPO_URL = 'https://github.com/juga0/page-watcher-data'
DATA_REPO_NAME = 'page-watcher-data'


def main():
    write_ssh_keys(SSH_DIR, environ(MORPH_SSH_PRIV_KEY_ENV),
                   environ(MORPH_SSH_PUB_KEY_ENV), SSH_PRIV_KEY_PATH,
                   SSH_PUB_KEY_PATH)
    write_ssh_command(GIT_SSH_COMMAND_PATH, GIT_SSH_COMMAND_MORPHIO)
    write_ssh_key_server(SSH_PUB_KEY_SERVER, SSH_PUB_KEY_SERVER_PATH)
    repo = pull_or_clone(DATA_REPO_PATH, DATA_REPO_URL,
                         DATA_REPO_BRANCH, DATA_REPO_NAME,
                         GIT_SSH_COMMAND_PATH, False)
    check_ssh_keys(repo, GIT_SSH_COMMAND_PATH, SSH_PRIV_KEY_PATH,
                   SSH_PUB_KEY_PATH, SSH_PUB_KEY_SERVER_PATH)

if __name__ == "__main__":
    main()
