import json
import click
import re
import sys
from bumper.default_conf import default_conf
import bumper.file_updater as file_updater
import bumper.gitops as gitops
import semver


class BumperContext(object):
    conf = None


@click.group()
@click.pass_context
@click.version_option(version="0.1.0")
def cli(ctx):
    try:
        conf = merge_config_with_default(conf)
    except:
        conf = default_conf
    bctx = BumperContext()
    bctx.conf = conf
    ctx.obj = bctx


def parse_config_file():
    with open('bumper.json', 'r') as conf_file:
        d = json.loads(conf_file.read())
    return d


def merge_config_with_default():
    config = parse_config_file()
    for k in config.keys():
        default_conf[k] = config[k]
    return default_conf


@cli.command()
@click.pass_obj
@click.argument('version')
def up_version(ctx, **kwargs):
    try:
        latest_version = gitops.get_latest_tag()
    except:
        print('Unable to get latest tag from repo')
        latest_version = ctx.conf['version']['initial']

    if kwargs['version'] in ctx.conf['version']['increments']:
        version = bump_it(latest_version, kwargs['version'])
    else:
        try:
            version = semver.parse(kwargs['version'])
        except ValueError:
            print("Supplied version is not a valid SemVer string or increment")
            sys.exit(1)

        print(version)

    apply_bump(version)


def bump_it(latest_version, increment):
    func = 'bump_{}'.format(increment)
    return semver.__dict__[func](latest_version)


def apply_bump(version):
    print(version)


def main():
    if gitops.is_repo_dirty():
        print('Repo is dirty. Cannot continue')
        sys.exit(1)

    cli()
    return
    print(conf)

    try:
        latest_tag = gitops.get_latest_tag()
    except:
        print('Unable to get latest tag from repo')

        latest_tag = conf['version']['initial']

    new_version = semver.bump_minor(latest_tag)

    file_updater.update_files(conf, new_version)

    gitops.create_commit(new_version)
    gitops.create_new_tag(new_version)