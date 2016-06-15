from os.path import join, abspath, dirname

BASE_PATH = abspath(__file__)
ROOT_PATH = dirname(BASE_PATH)
DATA_REPO = 'page-watcher-data'
DATA_REPO_PATH = join(ROOT_PATH, DATA_REPO)

SSH_DIR = 'ssh'
SSH_PATH = join(ROOT_PATH, SSH_DIR)
SSH_PRIV_KEY_PATH = join(SSH_PATH, 'id_rsa')
SSH_PUB_KEY_PATH = join(SSH_PATH, 'id_rsa.pub')

GIT_SSH_COMMAND_FILE = 'ssh_command.sh'
GIT_SSH_COMMAND_PATH = join(ROOT_PATH, GIT_SSH_COMMAND_FILE)

GITHUB_SSH_PUB_KEY = 'github.com ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAq2A7hRGmd\
nm9tUDbO9IDSwBK6TbQa+PXYPCPy6rbTrTtw7PHkccKrpp0yVhp5HdEIcKr6pLlVDBfOLX9QUs\
yCOV0wzfjIJNlGEYsdlLJizHhbn2mUjvSAHQqZETYP81eFzLQNnPHt4EVVUh7VfDESU84KezmD\
5QlWpXLmvU31/yMf+Se8xhHTvKSCZIFImWwoG6mbUoWf9nzpIoaSjB+weqqUUmpaaasXVal72J\
+UX2B+2RPW3RcT0eOzQgqlJL3RKrTJvdsjE3JEAvGq3lGHSZXy28G3skua2SmVi/w4yCE6gbOD\
qnTWlg7+wC604ydGXA8VJiS5ap43JXiUFFAaQ=='
SSH_PUB_KEY_SERVER_PATH = join(SSH_PATH, 'ssh_pub_key_server')

MORPH_SSH_PRIV_KEY_ENV = 'MORPH_SSH_PRIV_KEY'
MORPH_SSH_PUB_KEY_ENV = 'MORPH_SSH_PUB_KEY'

GIT_SSH_COMMAND = '#!/bin/sh\nssh -o "ProxyCommand=nc -X 5 -x 127.0.0.1:9050 %h %p" -i ' + SSH_PRIV_KEY_PATH + \
    ' -o "UserKnownHostsFile ' + SSH_PUB_KEY_SERVER_PATH + '" "$@"\n'
GIT_SSH_COMMAND_MORPHIO = '#!/bin/sh\nssh -i ' + SSH_PRIV_KEY_PATH + \
    ' -o "UserKnownHostsFile ' + SSH_PUB_KEY_SERVER_PATH + \
    '" -o "StrictHostKeyChecking no"' + \
    ' "$@"\n'
