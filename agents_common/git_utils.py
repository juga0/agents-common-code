# -*- coding: utf-8 -*-

from git import Repo, InvalidGitRepositoryError, GitCmdObjectDB, \
    GitCommandError
from os import environ
from os.path import isdir
import sys
from shutil import rmtree
import time
import logging

logger = logging.getLogger(__name__)


def pull_or_clone(repo_path, repo_url, repo_branch,
                  repo_name='origin', git_ssh_command_path=None,
                  exit_on_error=True):
    repo = None
    logger.debug("OBTAINING REPO")
    if isdir(repo_path):
        logger.debug('found dir %s' % repo_path)
        try:
            repo = Repo(repo_path, odbt=GitCmdObjectDB)
            logger.debug('dir is a repo')
            origin = repo.remotes[repo_name]
        # dir exist but is not a repo
        except InvalidGitRepositoryError, e:
            logger.exception(e)
            rmtree(repo_path)
            try:
                repo, origin = clone_repo(repo_url, repo_path, repo_branch,
                                          repo_name, git_ssh_command_path)
            except GitCommandError, e:
                # FIXME: handle in a better way exception
                logger.exception(e)
                logger.debug('cant obtain repo')
                if exit_on_error:
                    sys.exit()
                else:
                    repo, origin = create_repo(repo_path, repo_name, repo_url)
        else:
            pull_repo(origin, repo_branch, git_ssh_command_path)
            # FIXME: pull fail?
        return repo
    try:
        repo, origin = clone_repo(repo_url, repo_path, repo_branch,
                                  repo_name, git_ssh_command_path)
    except GitCommandError, e:
    # FIXME: handle better exception
        logger.exception(e)
        logger.debug('cant obtain repo')
        if exit_on_error:
            sys.exit()
        else:
            repo, origin = create_repo(repo_path, repo_name, repo_url)
    return repo


def pull_repo(origin_repo, repo_branch, git_ssh_command_path=None):
    logger.info("PULLING")
    logger.info('repository %s in %s' % (origin_repo.url, origin_repo.name))
    try:
        if git_ssh_command_path:
            logger.debug('pulling with git_ssh_command_path %s' %
                         git_ssh_command_path)
            with origin_repo.repo.git.custom_environment(
                    GIT_SSH=git_ssh_command_path):
                origin_repo.pull(repo_branch)
        else:
            logger.debug('pulling without git_ssh_command_path')
            origin_repo.pull(repo_branch)
    except GitCommandError, e:
        # FIXME: handle better exception
        logger.exception(e)
        raise e


def clone_repo(repo_url, repo_path, repo_branch, repo_name,
               git_ssh_command_path=None):
    logger.info("CLONING")
    logger.info('repository %s in %s' % (repo_url, repo_name))
    try:
        if git_ssh_command_path:
            logger.debug('pulling with git_ssh_command_path %s' %
                         git_ssh_command_path)
            repo = Repo.clone_from(repo_url, repo_path, branch=repo_branch,
                                   env={'GIT_SSH': git_ssh_command_path})
        else:
            logger.debug('pulling without git_ssh_command_path')
            repo = Repo.clone_from(repo_url, repo_path, branch=repo_branch)
        origin = repo.remotes['origin']
        origin.rename(repo_name)
        return repo, origin
    except GitCommandError, e:
        # FIXME: handle better exception
        logger.exception(e)
        raise e


def create_repo(repo_path, repo_name, repo_url):
    logger.info("CREATING REPO")
    logger.info('repository %s in %s' % (repo_url, repo_name))
    repo = Repo.init(repo_path)
    origin = repo.create_remote(repo_name, repo_url)
    return repo, origin


def commit_changes(repo, repo_author, repo_email):
    logger.info("COMMITING")
    if repo.index.diff(None) or repo.untracked_files:
        repo.index.add('*')
        logger.debug('added files to repo')
        commit_msg = "Crawl completed at " + time.strftime("%Y-%m-%d-%H-%M-%S")
        environ["GIT_AUTHOR_NAME"] = repo_author
        environ["GIT_AUTHOR_EMAIL"] = repo_email
        # commit only if something changed
        committed = repo.index.commit(commit_msg)
        logger.info('commited policy data')
        logger.info(committed)
    else:
        logger.info('nothing changed, not committing/pushing')


def push_repo(repo, git_ssh_command_path, repo_branch):
        logger.info('PUSHING')
        logger.info('repository %s in %s' % (repo.remote().url,
                                             repo.remote().name))
        # FIXME: there could be more than 1 origin
        origin = repo.remotes[0]
        # origin = repo.remotes[repo_name]
        logger.debug('pushing with git_ssh_command_path %s' %
                     git_ssh_command_path)
        # more debugging for morph.io
        with open(git_ssh_command_path) as f:
            logger.debug('ssh command content %s' % f.read())
        with origin.repo.git.custom_environment(GIT_SSH=git_ssh_command_path):
            environ['GIT_SSH'] = git_ssh_command_path
            logger.debug('GIT_SSH %s' % environ.get('GIT_SSH'))
            logger.debug('GIT_SSH_COMMAND %s' % environ.get('GIT_SSH_COMMAND'))
            try:
                origin.push(repo_branch)
            except GitCommandError, e:
                # FIXME: handle better exception
                logger.exception(e)
