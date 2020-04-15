from git import Repo
import os
import semver


def get_repo():
    """
    Get the repo for the current working directory.
    """
    return Repo(os.getcwd())


def get_username():
    """
    Return the username of the current repo
    """
    repo = get_repo()
    return repo.config_reader().get_value("user", "name")


def get_email():
    """
    Return the configured email of the current repo
    """
    repo = get_repo()
    return repo.config_reader().get_value("user", "email")


def is_repo_dirty():
    """
    Check if the current repo is dirty or not, including untracked files
    """
    repo = get_repo()
    return repo.is_dirty(untracked_files=True)


def get_latest_tag():
    """
    Get the latest tag that matches a semantic version. This is used to work
    out the original version from which to version up from
    """
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
    """
    Create a new tag given the new version and tagname string

    :new_version: string of new semantic version to use for tag
    :tag_name" the string to use in the tag's message
    """
    repo = get_repo()
    repo.create_tag(new_version, message=tag_name)


def create_commit(commit_msg):
    """
    create a commit with the given message

    :commit_msg: string to use for the commit message
    """
    repo = get_repo()
    index = repo.index
    changed_files = [item.a_path for item in repo.index.diff(None)]
    index.add(repo.untracked_files + changed_files)
    repo.git.commit("-m", commit_msg)


def get_commit_messages():
    """
    Get all the commit messages since the last versup run.
    Uses the output of the git log to the last versup tag, and returns
    the headers for those commits to be used in the changelog
    """
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
        if len(split_commit) < 2:
            return out
        data["hash"] = split_commit[0]
        data["author_name"] = split_commit[1]
        data["author_email"] = split_commit[2]
        data["date"] = split_commit[3]
        data["message"] = split_commit[4]

        out.append(data)
    return out
