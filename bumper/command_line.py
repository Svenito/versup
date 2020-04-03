import sys
import os
import click
import semver

from bumper import __version__
from bumper.conf_reader import (
    get_conf_value,
    merge_configs_with_default,
    parse_config_file,
)
from bumper.custom_cmd_group import DefaultCommandGroup
import bumper.file_updater as file_updater
import bumper.gitops as gitops
import bumper.template as template
import bumper.changelog as changelog
import bumper.script_runner as script_runner


class BumperContext(object):
    conf = None
    template = None
    version = None


@click.group(cls=DefaultCommandGroup)
@click.pass_context
# @click.version_option(version=__version__)
def cli(ctx, **kwargs):
    bobj = BumperContext()
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
        config = parse_config_file("./.bumper.json")
    if kwargs["global"]:
        config = parse_config_file("~/.config/bumper.json")
    pprint.pprint(config)


@cli.command(default_command=True)
@click.pass_context
@click.argument("increment")
def do_bump(ctx, **kwargs):
    """
    INCREMENT Bump up version in all documents, make commit, tag commit,
    and optionally create changelog
    """
    ctx.obj.version = kwargs["increment"]
    if not ctx.obj.version in get_conf_value(ctx.obj.conf, "version/increments"):
        try:
            # Parse to see if version format is ok
            semver.parse_version_info(ctx.obj.version)
        except ValueError:
            print("ERROR WITH VERSION ARG")
            return

    version = get_new_version(ctx.obj.conf, ctx.obj.version)

    apply_bump(ctx.obj.conf, version)


@script_runner.prepost_script("bump")
def apply_bump(config, version):
    # Run through all stages of a release

    # Update the files specified in config
    files_to_update = get_conf_value(config, "files")
    file_updater.update_files(version, files_to_update)

    # create changelog
    if get_conf_value(config, "changelog/enabled"):
        do_changelog(config, version)

    # create new commit with version
    if get_conf_value(config, "commit/enabled"):
        commit(config, version)

    # tag commit
    if get_conf_value(config, "tag/enabled"):
        tag(config, version)


def bump_version(latest_version, increment):
    func = "bump_{}".format(increment)
    return semver.__dict__[func](latest_version)


def get_new_version(config, version):
    """
    :version: is either an increment or a semantic version. Given an increment
    the current version (based on the latest git commit, or the initial version
    from the config) is incremented.
    Given a version, that version is used as is provided it is valid
    """
    if gitops.is_repo_dirty():
        print("Repo is dirty. Cannot continue")
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
            print("Supplied version is not a valid SemVer string or increment")
            sys.exit(1)

    # Update value in template data struct
    template.token_data["version"] = new_version

    return new_version


@script_runner.prepost_script("changelog")
def do_changelog(config, version):
    changelog_file = get_conf_value(config, "changelog/file")
    # If no changelog file and create is off, prompt
    if not os.path.isfile(changelog_file):
        if not get_conf_value(config, "changelog/create"):
            if not click.confirm("No changelog file found. Create it?"):
                return
            # Ok to create/update it now
    changelog.write(config, version)


@script_runner.prepost_script("commit")
def commit(config, version):
    if not gitops.is_repo_dirty():
        print("No unstaged changes to repo. Cannot make a commit.")
        # sys.exit(1)
    gitops.create_commit(version, config)


@script_runner.prepost_script("tag")
def tag(config, version):
    if gitops.is_repo_dirty():
        print("Unstaged changes to repo. Cannot make a tag.")
        sys.exit(1)
    gitops.create_new_tag(version, config)


def main():
    cli()
