from git import Repo
import os
import bumper.template as template
from bumper.conf_reader import get_conf_value
import semver


def get_repo():
    return Repo(os.getcwd())


def is_repo_dirty():
    repo = get_repo()
    return repo.is_dirty()


def get_latest_tag():
    repo = get_repo()
    latest_tags = repo.git.tag(sort="-creatordate").split("\n")[:10]
    for tag in latest_tags:
        try:
            semver.parse_version_info(tag)
        except ValueError:
            continue
        return tag

    raise ValueError


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


def get_commit_messages():
    # git log --pretty=oneline HEAD...0.2.0
    latest_tag = get_latest_tag()
    repo = get_repo()
    commits = repo.git.log(
        "--pretty=format:%H||%an||%ae||%at||%s", "HEAD...{}".format(latest_tag)
    ).split("\n")
    out = []
    for commit in commits:
        data = dict()
        split_commit = commit.split("||")
        print(split_commit)
        data["hash"] = split_commit[0]
        data["author_name"] = split_commit[1]
        data["author_email"] = split_commit[2]
        data["date"] = split_commit[3]
        data["msg"] = split_commit[4]

        out.append(data)
    return out
