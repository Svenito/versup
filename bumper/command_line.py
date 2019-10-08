import json
import click
import re
import sys
import os
from bumper.conf_reader import get_conf_value
from bumper.custom_cmd_group import DefaultCommandGroup
import bumper.file_updater as file_updater
import bumper.gitops as gitops
import bumper.template as template
import semver

__version__ = "0.0.1"

class BumperContext(object):
    conf = None
    version = None


@click.group(cls=DefaultCommandGroup)
@click.pass_context
@click.version_option(version=__version__)
def cli(ctx, **kwargs):
    conf_reader.merge_config_with_default()


@cli.command(default_command=True)
@click.pass_context
@click.argument("increment")
def do_bump(ctx, **kwargs):
    """
    Bump up version in all documents, make commit, tag commit,
    and optionally create changelog
    """
    increment = kwargs["increment"]
    if not increment in get_conf_value("version/increments"):
        try:
            # Parse to see if format is ok
            semver.parse_version_info(increment)
        except ValueError:
            print("ERROR WITH VERSION ARG")
            return

    ctx.invoke(version, version=increment)


def bump_version(latest_version, increment):
    func = "bump_{}".format(increment)
    return semver.__dict__[func](latest_version)


@cli.command()
@click.pass_context
@click.argument("version")
def version(ctx, **kwargs):
    if gitops.is_repo_dirty():
        print("Repo is dirty. Cannot continue")
        # TODO raise exception
        sys.exit(1)

    try:
        latest_version = gitops.get_latest_tag()
    except:
        latest_version = get_conf_value("version/initial")

    if kwargs["version"] in get_conf_value("version/increments"):
        version = bump_version(latest_version, kwargs["version"])
    else:
        try:
            semver.parse_version_info(kwargs["version"])
            version = kwargs["version"]
        except ValueError:
            print("Supplied version is not a valid SemVer string or increment")
            sys.exit(1)

    # Update value in template data struct
    template.token_data['version'] = version
    ctx.obj.version = version
    # Do the work
    apply_bump(ctx)


def apply_bump(ctx):
    # Run through all stages of a release
    file_updater.update_files(ctx.obj.version)

    # create new commit with version
    if get_conf_value("commit/enabled"):
        ctx.invoke(commit, version=version)

    # tag commit
    #ctx.invoke(tag, version=version)
    # create changelog.


@cli.command()
@click.pass_context
def commit(ctx, **kwargs):
    if not gitops.is_repo_dirty():
        print("No unstaged changes to repo. Cannot make a commit.")
        #sys.exit(1)
    gitops.create_commit(kwargs['version'])


@cli.command()
@click.pass_context
def tag(ctx, **kwargs):
    if gitops.is_repo_dirty():
        print("Unstaged changes to repo. Cannot make a tag.")
        sys.exit(1)
    gitops.create_new_tag(kwargs['version'])


@cli.command()
@click.pass_context
def changelog(ctx, **kwargs):
    print("changelog")
    pass


@cli.command()
def release():
    pass


def main():
    cli()