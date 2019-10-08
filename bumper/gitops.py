from git import Repo
import os


def get_repo():
    return Repo(os.getcwd())


def is_repo_dirty():
    repo = get_repo()
    return repo.is_dirty()


def get_latest_tag():
    repo = get_repo()
    latest_tag = repo.git.tag(sort="creatordate").split("\n")[-1]
    return latest_tag


def create_new_tag(new_version, conf):
    repo = get_repo()
    # TODO: configurable tag message
    repo.create_tag(new_version, message="[Bumper] tagged '{0}'".format(new_version))


def create_commit(new_version, conf):
    repo = get_repo()
    files = repo.git.diff(None, name_only=True)
    for f in files.split("\n"):
        repo.git.add(f)
    # TODO: configurable commit message
    commit_msg = "[Bumper] Set version to {}".format(new_version)

    repo.git.commit("-m", commit_msg)