import sys
import os
import click
import datetime

from versup import __version__
from versup.conf_reader import (
    get_conf_value,
    merge_configs_with_default,
    parse_config_file,
)
from versup import VersupError
from versup.custom_cmd_group import DefaultCommandGroup
import versup.file_updater as file_updater
import versup.gitops as gitops
import versup.template as template
import versup.changelog as changelog
import versup.script_runner as script_runner
from versup.printer import print_ok, print_error, print_warn
from versup.versioning import get_new_version

CONTEXT_SETTINGS = dict(
    help_option_names=["-h", "--help"],
)


class VersupContext(object):
    conf = None
    template = None
    version = None


@click.group(cls=DefaultCommandGroup, context_settings=CONTEXT_SETTINGS)
@click.pass_context
@click.version_option(version=__version__)
def cli(ctx, **kwargs):
    bobj = VersupContext()
    bobj.conf = merge_configs_with_default()
    bobj.template_data = template.token_data
    ctx.obj = bobj


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.pass_context
@click.option("-l", "--local", is_flag=True, help="Show local configuration options")
@click.option("-g", "--global", is_flag=True, help="Show global configuration options")
def show_config(ctx, **kwargs):
    import pprint

    config = ctx.obj.conf
    if kwargs["local"]:
        config = parse_config_file("./.versup.json")
    if kwargs["global"]:
        config = parse_config_file("~/.config/versup.json")
    pprint.pprint(config)


@cli.command(
    default_command=True, name="increment/version", context_settings=CONTEXT_SETTINGS
)
@click.pass_context
@click.argument("increment")
@click.option("--no-commit", is_flag=True, help="Skip making commit")
@click.option("--no-changelog", is_flag=True, help="Skip changelog update")
@click.option("--no-tag", is_flag=True, help="Skip creating tag")
@click.option("--no-fileupdate", is_flag=True, help="Skip updating files")
@click.option(
    "-n",
    "--dryrun",
    is_flag=True,
    help="Show what will be done without applying anything",
)
def do_versup(ctx, **kwargs):
    """
    Increment or set project version
    """
    current_branch = gitops.get_current_branch()
    target_branch = get_conf_value(ctx.obj.conf, "commit/mainbranch")
    if not gitops.check_current_branch_matches(target_branch):
        print_warn(
            "Main branch set to '{0}'. Currently on '{1}'".format(
                target_branch, current_branch
            )
        )
        if not kwargs["dryrun"] and not click.confirm("Continue anyway?"):
            return

    ctx.obj.version = kwargs["increment"]

    try:
        try:
            latest_version = gitops.get_latest_tag()
        except ValueError:
            latest_version = get_conf_value(ctx.obj.conf, "version/initial")
            print_warn(
                "No previous version tag found. Using initial value from config: {}.".format(
                    latest_version
                )
            )
        version = get_new_version(
            latest_version,
            ctx.obj.version,
            get_conf_value(ctx.obj.conf, "version/increments"),
            kwargs["dryrun"],
        )
    except VersupError as e:
        print_error(str(e))
        return

    # Update the token_data with what we know
    template.token_data["version"] = version

    today = datetime.date.today()
    template_date = today.strftime(get_conf_value(ctx.obj.conf, "tokens/date/format"))
    template.token_data["date"] = template_date

    template_date = today.strftime(
        get_conf_value(ctx.obj.conf, "tokens/version_date/format")
    )
    template.token_data["version_date"] = template_date

    template.token_data["author_name"] = gitops.get_username()
    template.token_data["author_email"] = gitops.get_email()

    template.token_data["message"] = get_conf_value(ctx.obj.conf, "commit/message")

    apply_bump(ctx.obj.conf, version, **kwargs)


@script_runner.prepost_script("bump")
def apply_bump(config, version, **kwargs):
    """
    Runs through all the stages of the release as defined by the config file.
    """
    # Update the files specified in config
    if not kwargs["no_fileupdate"]:
        files_to_update = get_conf_value(config, "files")
        updated = file_updater.update_files(version, files_to_update, kwargs["dryrun"])
        print_ok("Updated {}".format(", ".join(updated)))

    # create changelog
    if not kwargs["no_changelog"] and get_conf_value(config, "changelog/enabled"):
        do_changelog(config, version, **kwargs)

    # create new commit with version
    if not kwargs["no_commit"] and get_conf_value(config, "commit/enabled"):
        commit(config, version, **kwargs)

    # tag commit (only if a commit is made)
    if (
        not kwargs["no_commit"]
        and not kwargs["no_tag"]
        and get_conf_value(config, "tag/enabled")
    ):
        tag(config, version, **kwargs)


@script_runner.prepost_script("changelog")
def do_changelog(config, version, **kwargs):
    """
    Write the changelog file if config is set to write it. If it
    does not exist, prompt user if they want to create it, if "create changelog"
    is True in the config.
    """
    if not get_conf_value(config, "changelog/enabled"):
        return
    changelog_config = get_conf_value(config, "changelog")
    changelog_file = changelog_config["file"]
    # If no changelog file and create is off, prompt
    if not kwargs["dryrun"] and not os.path.isfile(changelog_file):
        if not changelog_config["create"]:
            if not click.confirm("No changelog file found. Create it?"):
                return
            # Ok to create/update it now
    changelog.write(
        changelog_file,
        changelog_config["version"],
        changelog_config["commit"],
        changelog_config["separator"],
        changelog_config["open"],
        version,
        kwargs["dryrun"],
    )
    print_ok("Changelog updated")


@script_runner.prepost_script("commit")
def commit(config, version, **kwargs):
    """
    Create the version up commit if enabled in the config
    """
    if not get_conf_value(config, "commit/enabled"):
        return

    if not kwargs["dryrun"] and not gitops.is_repo_dirty():
        print("No unstaged changes to repo. Making no new commit.")
        return
    commit_config = get_conf_value(config, "commit")
    template.token_data["version"] = version
    commit_msg = template.render(commit_config["message"])
    if kwargs["dryrun"]:
        print("Create commit with commit msg: {}".format(commit_msg))
    else:
        gitops.create_commit(commit_msg)
    print_ok("Commit created")


@script_runner.prepost_script("tag")
def tag(config, version, **kwargs):
    """
    Tag the latest commit with the new version release
    """
    if not get_conf_value(config, "tag/enabled"):
        return

    if not kwargs["dryrun"] and gitops.is_repo_dirty():
        print("Unstaged changes to repo. Cannot make a tag.")
        sys.exit(1)
    tag_config = get_conf_value(config, "tag")
    template.token_data["version"] = version
    tag_name = template.render(tag_config["name"])
    if kwargs["dryrun"]:
        print("Create tag {} with msg {}".format(version, tag_name))
    else:
        gitops.create_new_tag(version, tag_name)

    print_ok("Tag {} created".format(tag_name))


def main():
    cli(prog_name="versup")
