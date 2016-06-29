# -*- coding: utf-8 -*-

from git import Repo, GitCmdObjectDB
from os import environ, makedirs, listdir
from os.path import isdir, join, isfile, splitext
from yaml_utils import read_yaml
from system_utils import now
import logging

logger = logging.getLogger(__name__)


def obtain_policy_type_from_filename(file_path):
    policy_type = None
    logger.debug('file_path %s' % file_path)
    if file_path.endswith('.yml'):
        policy_type = splitext(file_path.lower())[0]
    logger.debug('policy_type %s' % policy_type)
    return policy_type


def create_data_file_path(rule, data_path):
    data_dir_path = join(data_path,
                     rule.get('organization'),
                     rule.get('tool'))
    logger.debug('data_dir_path: %s' % data_dir_path)
    if not isdir(data_dir_path):
        makedirs(data_dir_path)
        logger.debug('created data_dir_path')
    data_file_path = join(data_dir_path, rule.get('policy') + '.txt')
    return data_file_path


# def create_metadata_data_file_path(rule, data_path):
#     data_dir_path = join(data_path,
#                          rule.get('organization'),
#                          rule.get('tool'))
#     if not isdir(data_dir_path):
#         makedirs(data_dir_path)
#     metadata_file_path = join(data_dir_path, rule.get('policy')
#                               + '_metadata.txt')
#     logger.debug('metadata file path %s' % metadata_file_path)
#     return metadata_file_path


def write_metadata_file(metadata_path, repo_path):
    from yaml_utils import generate_yaml
    metadata = generate_metadata(repo_path)
    metadata_yaml = generate_yaml(metadata)
    with open(metadata_path, 'w') as f:
        f.write(metadata_yaml)
    logger.debug('wroten %s with %s' % (metadata_path, metadata_yaml))


def yamlfilelist(dir_path):
    files = []
    for f in listdir(dir_path):
        fulldir = join(dir_path, f)
        if isdir(fulldir):
            flist = [join(fulldir, x) for x in listdir(fulldir)
                     if isfile(join(fulldir, x)) and x.endswith('.yml')]
            files.extend(flist)
            files.extend(yamlfilelist(fulldir))
    return files


def obtain_yaml_from_path(repo_path):
    from yaml_utils import read_yaml
    from data_structures_utils import merge_two_dicts
    from os.path import sep
    yaml_list = []
    files_path = yamlfilelist(repo_path)
    for file_path in files_path:
        path_list = file_path.split(sep)
        path_dict = {
            'policy': obtain_policy_type_from_filename(path_list[-1]),
            'tool': path_list[-2],
            'organization': path_list[-3]
        }
        yaml_data = read_yaml(file_path)
        if yaml_data:
            yaml_dict = merge_two_dicts(yaml_data, path_dict)
            yaml_list.append(yaml_dict)
    logger.debug(yaml_list)
    return yaml_list


def obtain_yaml(repo_path, repo_url, repo_branch, file_path=None,
        repo_name='origin', git_ssh_command_path=None,
        exit_on_error=True):
    from git_utils import pull_or_clone
    logger.debug('repo_name %s' % repo_name)
    logger.debug('git_ssh_command_path: %s' % git_ssh_command_path)
    pull_or_clone(repo_path, repo_url, repo_branch,
                  repo_name, git_ssh_command_path,
                  exit_on_error)
    logger.debug('file_path %s' % file_path)
    if file_path:
        yaml_data = read_yaml(file_path)
        return yaml_data
    yaml_data = obtain_yaml_from_path(repo_path)
    return yaml_data


def commit_push_if_changes(repo, repo_author, repo_email, git_ssh_command_path,
           repo_branch, metadata_path):
    # FIXME: handle changes to be commited
    # if repo.index.diff(repo.head.commit):
    #     logger.debug('there are unpushed changes')
    from git_utils import commit_changes, push_repo
    if repo.index.diff(None) or repo.untracked_files:
        write_metadata_file(metadata_path, repo.working_dir)
        commit_changes(repo, repo_author, repo_email)
        push_repo(repo, git_ssh_command_path, repo_branch)
    else:
        logger.debug('nothing changed, not committing/pushing')


def obtain_script_commit_hash(script_path):
    # FIXME: ROOT_PATH
    script_repo = Repo(script_path, odbt=GitCmdObjectDB)
    commit_hash = script_repo.head.commit.hexsha
    logger.debug(commit_hash)
    return commit_hash


def generate_host_identifier():
    from system_utils import obtain_uname
    hostid = generate_hash(obtain_uname())
    logger.debug(hostid)
    return hostid


def generate_metadata(repo_path):
    from system_utils import obtain_public_ip, obtain_uname, hasproxy
    # ADVICE: system information is sensitive
    # in morph.io or running with tor, the ip will change all the time
    # FIXME: in morph.io cant obtain the current git revision this way
    # in morph.io host name will change all the time
    # an env variable that doesnt change is HOME=/app
    if ismorpio():
        ip = obtain_public_ip()
        uname = obtain_uname()
        commit_revision = None
        host = 'morph.io'
    elif hasproxy():
        ip = obtain_public_ip()
        uname = generate_hash(obtain_uname())
        commit_revision = obtain_script_commit_hash(repo_path)
        host = 'local'
    else:
        ip = generate_hash(obtain_public_ip())
        uname = generate_hash(obtain_uname())
        commit_revision = obtain_script_commit_hash(repo_path)
        host = 'dev server'
    metadata = {
        'timestamp': str(now()),
        'ip': ip,
        'uname': uname,
        'commit_revision': commit_revision,
        'host': host
    }
    logger.debug(metadata)
    return metadata


def generate_hash(text, encoding='utf-8'):
    import hashlib
    logger.debug('type text %s', type(text))
    if isinstance(text, unicode):
        logger.debug('text is unicode')
        text = text.encode(encoding)
        logger.debug('type text %s', type(text))
    sha = hashlib.sha256(text)
    sha_hex = sha.hexdigest()
    logger.debug(sha_hex)
    return sha_hex


def obtain_script_version():
    from pkg_resources import get_distribution, DistributionNotFound
    try:
        _dist = get_distribution('page-watcher-scraper')
    except DistributionNotFound:
        __version__ = 'Please install this project with setup.py'
    else:
        __version__ = _dist.version
    logger.debug(__version__)


def ismorpio():
    if environ['HOME'] == '/app':
        logger.debug('running in morph.io')
        return True
    else:
        logger.debug('not running in morph.io')
        return False
