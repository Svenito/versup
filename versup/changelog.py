from __future__ import print_function
import versup.gitops as gitops
import versup.template as template
import os
import sys
from typing import List, Dict


def show_file(changelog_file: str):
    """
    Open the supplied file with $EDITOR

    :changelog_file: The path to the file to open.

    """
    try:
        if sys.platform == "win32":
            os.system(f"notepad.exe {changelog_file}")
        else:
            editor = os.getenv("EDITOR", "vi")
            os.system(f"{editor} {changelog_file}")
    except Exception:
        pass


def write(
    changelog_file: str,
    version_line: str,
    changelog_line: str,
    separator: str,
    show: bool,
    version: str,
    dryrun: bool = False,
):
    """
    Write the new changelog file. Parses the commit messages and prepends the
    commits to the original text and saves out the file.
    Creates the file if it doesn't exist

    :changelog_file: Path and name of changelog file
    :version_line: The template string for the version number line
    :changelog_line: The template string for the changlog line entry
    :separator: The string to use to separate individual changelog entries
    :show: Whether to show the changelog when written or not
    :version: The new version to use
    :dryrun: Whether this is a dryrun. If true does not write file but
             prints new content to stdout

    """

    commits: List[Dict[str, str]] = gitops.get_commit_messages()

    if dryrun:
        print("Writing changelog entries:\n")
        for commit_data in commits:
            commit_data["hash"] = commit_data["hash"]
            commit_data["hash4"] = commit_data["hash"][:4]
            commit_data["hash7"] = commit_data["hash"][:7]
            commit_data["hash8"] = commit_data["hash"][:8]

            commit_line: str = template.render(changelog_line, commit_data)
            print(commit_line)
        print(separator)
    else:
        # Read original changelog
        original_data = ""
        try:
            with open(changelog_file, "r") as fh:
                original_data = fh.read()
        except IOError:
            original_data = ""

        version = template.render(version_line, {"version": version})
        with open(changelog_file, "w+") as fh:
            fh.write(version + "\n")
            for commit_data in commits:
                commit_data["hash"] = commit_data["hash"]
                commit_data["hash4"] = commit_data["hash"][:4]
                commit_data["hash7"] = commit_data["hash"][:7]
                commit_data["hash8"] = commit_data["hash"][:8]

                commit_line = template.render(changelog_line, commit_data)
                fh.write(commit_line + "\n")

            fh.write(separator + original_data)

        if show:
            show_file(changelog_file)
