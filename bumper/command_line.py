import json
import click
import re
import sys
import os
from bumper.default_conf import default_conf
from bumper.custom_cmd_group import DefaultCommandGroup
import bumper.file_updater as file_updater
import bumper.gitops as gitops
import semver

__version__ = "0.0.1"

class BumperContext(object):
    conf = None
    version = None


def command_tree(obj):
    if isinstance(obj, click.Group):
        return {name: command_tree(value)
            for name, value in obj.commands.items()}


def parse_config_file():
    cwd = os.getcwd()
    with open(os.path.join(cwd, "bumper.json"), "r") as conf_file:
        d = json.loads(conf_file.read())
    return d


def merge_config_with_default():
    print("")
    config = parse_config_file()
    for k in config.keys():
        default_conf[k] = config[k]
    return default_conf


@click.group(cls=DefaultCommandGroup)
@click.pass_context
@click.version_option(version=__version__)
def cli(ctx, **kwargs):
    try:
        conf = merge_config_with_default()
    except:
        conf = default_conf
    bctx = BumperContext()
    bctx.conf = conf
    ctx.obj = bctx


@cli.command(default_command=True)
@click.pass_context
@click.argument("increment")
def do_bump(ctx, **kwargs):
    """
    Bump up version in all documents, make commit, tag commit,
    and optionally create changelog
    """
    increment = kwargs["increment"]

    if increment in ctx.obj.conf["version"]["increments"]:
        print("do bump", increment)
    else:
        try:
            # Parse to see if format is ok
            semver.parse_version_info(increment)
            print (increment)
        except ValueError:
            print("no man")
            return
    ctx.invoke(version, version=increment)


def bump_it(latest_version, increment):
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
        print("Unable to get latest tag from repo")
        latest_version = ctx.obj.conf["version"]["initial"]

    if kwargs["version"] in ctx.obj.conf["version"]["increments"]:
        version = bump_it(latest_version, kwargs["version"])
    else:
        try:
            semver.parse_version_info(kwargs["version"])
            version = kwargs["version"]
        except ValueError:
            print("Supplied version is not a valid SemVer string or increment")
            sys.exit(1)

        print(version)
    ctx.obj.version = version
    apply_bump(ctx, version)


def apply_bump(ctx, version):
    print("APPLY:", version)
    file_updater.update_files(version, ctx.obj.conf)

    # create new commit with version
    ctx.invoke(commit, version=version)
    # tag commit
    ctx.invoke(tag, version=version)
    # create changelog.


@cli.command()
@click.pass_context
def commit(ctx, **kwargs):
    if not gitops.is_repo_dirty():
        print("No unstaged changes to repo. Cannot make a commit.")
        sys.exit(1)
    gitops.create_commit(kwargs['version'], ctx.obj.conf)
    pass


@cli.command()
@click.pass_context
def tag(ctx, **kwargs):
    if gitops.is_repo_dirty():
        print("Unstaged changes to repo. Cannot make a tag.")
        sys.exit(1)
    gitops.create_new_tag(kwargs['version'], ctx.obj.conf)


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