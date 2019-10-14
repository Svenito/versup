import json
import click
import re
import sys
import os
from bumper.conf_reader import get_conf_value, merge_configs_with_default
from bumper.custom_cmd_group import DefaultCommandGroup
import bumper.file_updater as file_updater
import bumper.gitops as gitops
import bumper.template as template
import bumper.changelog as changelog
import semver


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


@cli.command(default_command=True)
@click.pass_context
@click.argument("increment")
def do_bump(ctx, **kwargs):
    """
    Bump up version in all documents, make commit, tag commit,
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

    apply_bump(ctx)


def apply_bump(ctx):
    # Run through all stages of a release
    # Bump the version
    ctx.obj.version = ctx.invoke(version, version=ctx.obj.version)

    # create changelog
    if get_conf_value(ctx.obj.conf, "changelog/enabled"):
        ctx.invoke(do_changelog)

    # create new commit with version
    if get_conf_value(ctx.obj.conf, "commit/enabled"):
        ctx.invoke(commit)

    # tag commit
    ctx.invoke(tag)


def bump_version(latest_version, increment):
    func = "bump_{}".format(increment)
    return semver.__dict__[func](latest_version)


@cli.command()
@click.pass_context
@click.argument("version")
def version(ctx, **kwargs):
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
        latest_version = get_conf_value(ctx.obj.conf, "version/initial")

    # TODO: What happens if there's no latest version?
    if kwargs["version"] in get_conf_value(ctx.obj.conf, "version/increments"):
        ctx.obj.version = bump_version(latest_version, kwargs["version"])
    else:
        try:
            semver.parse_version_info(kwargs["version"])
            ctx.obj.version = kwargs["version"]
        except ValueError:
            print("Supplied version is not a valid SemVer string or increment")
            sys.exit(1)

    # Update value in template data struct
    template.token_data["version"] = ctx.obj.version

    # Update the files specified in config
    files_to_update = get_conf_value(ctx.obj.conf, "files")
    file_updater.update_files(ctx.obj.version, files_to_update)

    return ctx.obj.version


@cli.command()
@click.pass_context
def do_changelog(ctx, **kwargs):
    changelog_file = get_conf_value(ctx.obj.conf, "changelog/file")
    # If no changelog file and create is off, prompt
    if not os.path.isfile(changelog_file):
        if not get_conf_value(ctx.obj.conf, "changelog/create"):
            if not click.confirm("No changelog file found. Create it?"):
                return
            # Ok to create/update it now
    changelog.write(ctx.obj.conf, ctx.obj.version)


@cli.command()
@click.pass_context
def commit(ctx, **kwargs):
    if not gitops.is_repo_dirty():
        print("No unstaged changes to repo. Cannot make a commit.")
        # sys.exit(1)
    gitops.create_commit(ctx.obj.version, ctx.obj.conf)


@cli.command()
@click.pass_context
def tag(ctx, **kwargs):
    if gitops.is_repo_dirty():
        print("Unstaged changes to repo. Cannot make a tag.")
        sys.exit(1)
    gitops.create_new_tag(ctx.obj.version, ctx.obj.conf)


@cli.command()
def release():
    pass


def main():
    cli()
