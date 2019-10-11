from git import Repo
import os
import bumper.template as template
from bumper.conf_reader import get_conf_value


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
    template.token_data["version"] = new_version
    tag_name = template.render(get_conf_value(conf, "tag/name"))
    repo.create_tag(new_version, message=tag_name)


def create_commit(new_version, conf):
    repo = get_repo()
    files = repo.git.diff(None, name_only=True)
    for f in files.split("\n"):
        repo.git.add(f)

    template.token_data["version"] = new_version
    commit_msg = template.render(get_conf_value(conf, "commit/message"))

    repo.git.commit("-m", commit_msg)
