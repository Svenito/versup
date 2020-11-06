import semver

from versup import gitops
from versup.printer import print_warn
from versup import VersupError
from versup.conf_reader import get_conf_value


def bump_version(latest_version, increment):
    """
    bump the latest version by the given increment

    :version: the version number as a string
    :increment: the semantic increment as a string "minor, major etc"
    """
    latest = semver.VersionInfo.parse(latest_version)
    if increment == "release":
        if latest.prerelease:
            new_version = latest.next_version(part="patch")
        else:
            raise VersupError("No pre-release version found.")
    elif increment in ["prepatch", "preminor", "premajor"]:
        action = increment[3:]
        new_version = latest.next_version(part=action).bump_prerelease()
    else:
        new_version = latest.next_version(part=increment)
    return str(new_version)


def get_new_version(config, version, **kwargs):
    """
    version is either an increment or a semantic version. Given an increment
    the current version (based on the latest git commit, or the initial version
    from the config) is incremented.
    Given a version, that version is used as is provided it is valid
    """
    if gitops.is_repo_dirty():
        if kwargs["dryrun"]:
            print_warn("Repo is dirty.")
        else:
            raise VersupError("Repo is dirty. Cannot continue")

    try:
        latest_version = gitops.get_latest_tag()
    except ValueError:
        latest_version = get_conf_value(config, "version/initial")
        print_warn(
            "No previous version tag found. Using initial value from config: {}.".format(
                latest_version
            )
        )

    # TODO: What happens if there's no latest version?
    if version in get_conf_value(config, "version/increments"):
        # If bump version raises, let it bubble up
        new_version = bump_version(latest_version, version)
    else:
        try:
            semver.parse_version_info(version)
            new_version = version
        except ValueError:
            raise VersupError(
                "Supplied version is not a valid SemVer string or increment"
            )

    return new_version
