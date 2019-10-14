from bumper.conf_reader import get_conf_value
import bumper.gitops as gitops
import sys
import bumper.template as template
from subprocess import run, PIPE
import sys


def show_file(changelog_file):
    with open(changelog_file, "r") as fh:
        data = fh.read()

    try:
        pager = run(
            ["less", "-F", "-R", "-S", "-X", "-K"],
            stdout=sys.stdout,
            input=data,
            encoding="ascii",
        )
    except KeyboardInterrupt:
        # let less handle this, -K will exit cleanly
        pass


def write(conf, version):
    changelog_file = get_conf_value(conf, "changelog/file")
    commits = gitops.get_commit_messages()

    # Read original changelog
    with open(changelog_file, "r") as fh:
        original_data = fh.read()

    version = template.render(
        get_conf_value(conf, "changelog/version"), {"version": version}
    )
    with open(changelog_file, "w") as fh:
        fh.write(version + "\n")
        for commit_data in commits:
            commit_data["hash4"] = commit_data["hash"][:4]
            commit_data["hash7"] = commit_data["hash"][:7]
            commit_data["hash8"] = commit_data["hash"][:8]

            commit_line = template.render(
                get_conf_value(conf, "changelog/commit"), commit_data
            )
            fh.write(commit_line + "\n")

        fh.write(get_conf_value(conf, "changelog/separator") + original_data)

    if get_conf_value(conf, "changelog/open"):
        show_file(changelog_file)
