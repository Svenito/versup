from git import Repo
import os
import semver


def get_repo():
    return Repo(os.getcwd())


def get_username():
    repo = get_repo()
    return repo.config_reader().get_value("user", "name")


def get_email():
    repo = get_repo()
    return repo.config_reader().get_value("user", "email")


def is_repo_dirty():
    repo = get_repo()
    return repo.is_dirty(untracked_files=True)


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


def create_new_tag(new_version, tag_name):
    repo = get_repo()
    repo.create_tag(new_version, message=tag_name)


def create_commit(commit_msg):
    repo = get_repo()
    index = repo.index
    changed_files = [item.a_path for item in repo.index.diff(None)]
    index.add(repo.untracked_files + changed_files)
    repo.git.commit("-m", commit_msg)


def get_commit_messages():
    # git log --pretty=oneline HEAD...0.2.0
    try:
        latest_tag = get_latest_tag()
        commit_range = "HEAD...{}".format(latest_tag)
    except ValueError:
        commit_range = "HEAD"
    repo = get_repo()
    commits = repo.git.log("--pretty=format:%H||%an||%ae||%at||%s", commit_range).split(
        "\n"
    )
    out = []
    for commit in commits:
        data = dict()
        split_commit = commit.split("||")
        data["hash"] = split_commit[0]
        data["author_name"] = split_commit[1]
        data["author_email"] = split_commit[2]
        data["date"] = split_commit[3]
        data["message"] = split_commit[4]

        out.append(data)
    return out
