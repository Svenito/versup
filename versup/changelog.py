from __future__ import print_function
import versup.gitops as gitops
import versup.template as template
import os
import sys


def show_file(changelog_file):
    """
    Open the supplied file with $EDITOR

    :changelog_file: The path to the file to open.

    """
    try:
        if sys.platform == "win32":
            os.system("notepad.exe {}".format(changelog_file))
        else:
            editor = os.getenv("EDITOR", "vi")
            os.system("{} {}".format(editor, changelog_file))
    except Exception:
        pass


def write(
    changelog_file, version_line, changelog_line, separator, show, version, dryrun=False
):
    """
    Write the new changelog file. Gets the changelog filename (and optional
    path) from the config. Parses the commit messages and prepends the
    commits to the original text and saves out the file.
    Creates the file if there it doesn't exist

    :version: The new version to use
    :dryrun: Whether this is a dryrun. If true does not write file but
             prints new content to stdout

    """

    commits = gitops.get_commit_messages()

    if dryrun:
        print(u"Writing changelog entries:\n")
        for commit_data in commits:
            commit_data["hash"] = commit_data["hash"]
            commit_data["hash4"] = commit_data["hash"][:4]
            commit_data["hash7"] = commit_data["hash"][:7]
            commit_data["hash8"] = commit_data["hash"][:8]

            commit_line = template.render(changelog_line, commit_data)
            print(commit_line)
        print(separator)
    else:
        # Read original changelog
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
