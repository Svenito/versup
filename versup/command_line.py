import sys
import os
import click
import semver
import datetime

from versup import __version__
from versup.conf_reader import (
    get_conf_value,
    merge_configs_with_default,
    parse_config_file,
)
from versup.custom_cmd_group import DefaultCommandGroup
import versup.file_updater as file_updater
import versup.gitops as gitops
import versup.template as template
import versup.changelog as changelog
import versup.script_runner as script_runner
from versup.printer import print_ok, print_error, print_warn


class versupContext(object):
    conf = None
    template = None
    version = None


@click.group(cls=DefaultCommandGroup)
@click.pass_context
@click.version_option(version=__version__)
def cli(ctx, **kwargs):
    bobj = versupContext()
    bobj.conf = merge_configs_with_default()
    bobj.template_data = template.token_data
    ctx.obj = bobj


@cli.command()
@click.pass_context
@click.option("-l", "--local", is_flag=True)
@click.option("-g", "--global", is_flag=True)
def show_config(ctx, **kwargs):
    import pprint

    config = ctx.obj.conf
    if kwargs["local"]:
        config = parse_config_file("./.versup.json")
    if kwargs["global"]:
        config = parse_config_file("~/.config/versup.json")
    pprint.pprint(config)


@cli.command(default_command=True, name="increment/version")
@click.pass_context
@click.argument("increment")
@click.option("--no-commit", is_flag=True, help="Skip making commit")
@click.option("--no-changelog", is_flag=True, help="Skip changelog update")
@click.option("--no-tag", is_flag=True, help="Skip creating tag")
@click.option("-n", "--dryrun", is_flag=True, help="Show what will be done.")
def do_versup(ctx, **kwargs):
    """
    Increment or set project version
    """
    ctx.obj.version = kwargs["increment"]

    if not ctx.obj.version in get_conf_value(ctx.obj.conf, "version/increments"):
        try:
            # Parse to see if version format is ok
            semver.parse_version_info(ctx.obj.version)
        except ValueError:
            print_error("Supplied version is invalid")
            return

    version = get_new_version(ctx.obj.conf, ctx.obj.version, **kwargs)

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
    # Run through all stages of a release
    # Update the files specified in config
    files_to_update = get_conf_value(config, "files")
    file_updater.update_files(version, files_to_update)

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


def bump_version(latest_version, increment):
    func = "bump_{}".format(increment)
    return semver.__dict__[func](latest_version)


def get_new_version(config, version, **kwargs):
    """
    :version: is either an increment or a semantic version. Given an increment
    the current version (based on the latest git commit, or the initial version
    from the config) is incremented.
    Given a version, that version is used as is provided it is valid
    """
    if gitops.is_repo_dirty():
        if kwargs["dryrun"]:
            print_warn("Repo is dirty.")
        else:
            print_error("Repo is dirty. Cannot continue")
            # TODO raise exception
            sys.exit(1)

    try:
        latest_version = gitops.get_latest_tag()
    except:
        latest_version = get_conf_value(config, "version/initial")

    # TODO: What happens if there's no latest version?
    if version in get_conf_value(config, "version/increments"):
        new_version = bump_version(latest_version, version)
    else:
        try:
            semver.parse_version_info(version)
            new_version = version
        except ValueError:
            print_error("Supplied version is not a valid SemVer string or increment")
            sys.exit(1)

    # Update value in template data struct
    template.token_data["version"] = new_version

    return new_version


@script_runner.prepost_script("changelog")
def do_changelog(config, version, **kwargs):
    if not get_conf_value(config, "changelog/enabled"):
        return

    changelog_file = get_conf_value(config, "changelog/file")
    # If no changelog file and create is off, prompt
    if not kwargs["dryrun"] and not os.path.isfile(changelog_file):
        if not get_conf_value(config, "changelog/create"):
            if not click.confirm("No changelog file found. Create it?"):
                return
            # Ok to create/update it now
    changelog.write(config, version, kwargs["dryrun"])
    print_ok("Changelog updated")


@script_runner.prepost_script("commit")
def commit(config, version, **kwargs):
    if not get_conf_value(config, "commit/enabled"):
        return

    if not kwargs["dryrun"] and not gitops.is_repo_dirty():
        print("No unstaged changes to repo. Making no new commit.")
        return

    template.token_data["version"] = version
    commit_msg = template.render(get_conf_value(config, "commit/message"))
    if kwargs["dryrun"]:
        print("Create commit with commit msg: {}".format(commit_msg))
    else:
        gitops.create_commit(commit_msg)
    print_ok("Commit created")


@script_runner.prepost_script("tag")
def tag(config, version, **kwargs):
    if not get_conf_value(config, "tag/enabled"):
        return

    if not kwargs["dryrun"] and gitops.is_repo_dirty():
        print("Unstaged changes to repo. Cannot make a tag.")
        sys.exit(1)

    template.token_data["version"] = version
    tag_name = template.render(get_conf_value(config, "tag/name"))
    if kwargs["dryrun"]:
        print("Create tag {} with msg {}".format(version, tag_name))
    else:
        gitops.create_new_tag(version, tag_name)

    print_ok("Tag {} created".format(tag_name))


def main():
    cli()
