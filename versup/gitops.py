from git import Repo
import configparser
import os
import semver
from typing import List, Dict


class MissingConfig(Exception):
    pass


def get_repo() -> Repo:  # pragma: no cover
    """
    Get the repo for the current working directory.
    """
    return Repo(os.getcwd())


def get_username() -> str:  # pragma: no cover
    """
    Return the username of the current repo
    """
    repo = get_repo()
    try:
        return str(repo.config_reader().get_value("user", "name"))
    except (configparser.NoSectionError, configparser.NoOptionError):
        raise MissingConfig


def get_email() -> str:  # pragma: no cover
    """
    Return the configured email of the current repo
    """
    repo = get_repo()
    try:
        return str(repo.config_reader().get_value("user", "email"))
    except (configparser.NoSectionError, configparser.NoOptionError):
        raise MissingConfig


def get_current_branch() -> str:
    repo = get_repo()
    return repo.active_branch.name


def is_repo_dirty() -> bool:  # pragma: no cover
    """
    Check if the current repo is dirty or not, including untracked files
    """
    repo = get_repo()
    return repo.is_dirty(untracked_files=True)


def get_latest_tag() -> str:  # pragma: no cover
    """
    Get the latest tag that matches a semantic version. This is used to work
    out the original version from which to version up from
    It uses the `merged` option to only get tags from the currently active branch
    as branches might have different versioning paths.

    git --merged=<current branch> --sort=-creatordate
    """
    repo = get_repo()
    current_branch = get_current_branch()
    latest_tags = repo.git.tag(sort="-creatordate", merged=current_branch).split("\n")[
        :10
    ]
    for tag in latest_tags:
        try:
            semver.VersionInfo.parse(tag)
        except ValueError:
            continue
        return tag

    raise ValueError


def create_new_tag(new_version: str, tag_name: str):  # pragma: no cover
    """
    Create a new tag given the new version and tagname string

    :new_version: string of new semantic version to use for tag
    :tag_name: the string to use in the tag's message
    """
    repo = get_repo()
    repo.create_tag(new_version, message=tag_name)


def get_unstaged_changes() -> List[str]:
    repo = get_repo()
    changed_files: List[str] = [item.a_path for item in repo.index.diff(None)]
    return repo.untracked_files + changed_files


def create_commit(commit_msg: str, files_updated: List[str] = []):  # pragma: no cover
    """
    create a commit with the given message

    :commit_msg: string to use for the commit message
    """
    repo = get_repo()
    index = repo.index
    changed_files = [f.a_path for f in index.diff(None) if f.a_path in files_updated]
    index.add(changed_files)
    repo.git.commit("-m", commit_msg)


def get_commit_messages() -> List[Dict[str, str]]:
    """
    Get all the commit messages since the last versup run.
    Uses the output of the git log to the last versup tag, and returns
    the headers for those commits to be used in the changelog
    """
    # git log --pretty=oneline HEAD...0.2.0
    try:
        latest_tag = get_latest_tag()
        commit_range = f"HEAD...{latest_tag}"
    except ValueError:
        commit_range = "HEAD"
    repo = get_repo()
    commits = repo.git.log("--pretty=format:%H||%an||%ae||%at||%s", commit_range).split(
        "\n"
    )
    out: List[Dict[str, str]] = []

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


def check_current_branch_matches(expected_branch: str) -> bool:
    current_branch = get_current_branch()
    return current_branch == expected_branch
