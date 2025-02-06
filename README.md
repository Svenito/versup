> [!IMPORTANT]
> If you are viewing this on Github, this repo is a mirror from [Codeberg](https://codeberg.org/unlogic/versup)

# versup

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/versup/badge/?version=latest)](https://versup.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/versup.svg)](https://badge.fury.io/py/versup)
![Python application](https://github.com/Svenito/versup/workflows/Python%20application/badge.svg?branch=main)
[![Coverage Status](https://coveralls.io/repos/github/Svenito/versup/badge.svg?branch=main)](https://coveralls.io/github/Svenito/versup?branch=main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Bump your project version, update version numbers in your files, create a changelog,
make a commit, and tag it, all in one easy step. versup is also quite configurable.

# Install

Install as per normal package from PyPi

`pip install versup`

For development, clone this repo and run versup with

`uv run versup`

# Quick start

To get started all versup needs to know is the new version increment or number.
You can provide it with a valid semantic version increase such as `patch`, `minor`,
`major` etc, or an entirely new semantic version like `1.2.5`.

If you specifiy a version number, then versup will take that version and apply
it to the current project as is. If you provide an increment, it will get the
last version number from either the latest git tag that has a valid version,
or from the default version in the config file.

# Configuration

Versup has a default configuration which is shown below

```
{
    "force": False,  # Force the command without prompting the user
    "silent": False,  # Minimize the amount of logs
    "files": {},  # A map of `relativeFilePath: [regex, replacement, regexFlags?] | [regex, replacement, regexFlags?][]`
    "version": {
        "enabled": True,  # Bump the version number
        "initial": "0.0.0",  # Initial version
        "increments": [
            "major",
            "minor",
            "patch",
            "prerelease",
            "build",
        ],  # List of available increments to pick from
    },
    "changelog": {
        "enabled": True,  # Enable changelog auto-updates
        "create": False,  # Create the changelog file if it doesn"t exist
        "open": True,  # Open the changelog file after bumping
        "file": "CHANGELOG.md",  # Name of the changelog file
        "version": "### Version [version]",  # Template for the version line
        "commit": "- [message]",  # Template for the commit line
        "separator": "\n",  # Template for the separator between versions sections
    },
    "commit": {
        "enabled": True,  # Commit the changes automatically
        "message": "Update version to [version]",  # Template for the commit message
        "mainbranch": "master",  # name of the main development or release branch
    },
    "tag": {
        "enabled": True,  # Tag the bump commit
        "name": "v[version]",  # Template for the name of the tag in the tag message
    },
    "tokens": {
        "date": {
            "format": "%Y-%m-%d"  # Python datetime format to use when generating the `[date]` token
        },
        "version_date": {
            "format": "%Y-%m-%d"  # Python datetime format to use when generating the `[version_date]` token
        },
    },
    "scripts": {
        "prebump": "",  # Script to execute before bumping the version
        "postbump": "",  # Script to execute after bumping the version
        "prechangelog": "",  # Script to execute before updating the changelog
        "postchangelog": "",  # Script to execute after updating the changelog
        "precommit": "",  # Script to execute before committing
        "postcommit": "",  # Script to execute after committing
        "pretag": "",  # Script to execute before tagging
        "posttag": "",  # Script to execute after tagging
    },
}

```

If you want to override any settings, you can do this by creating a `~/.config/versup.json`
file or a `.versup.json` in your local project. Versup will read its default settings,
then merge in the global config (`~/.config/versup.json`), and finally
merge in the project level config.

# Template tags

In various places you can define what text to use for commit messages, or tags etc.
These support tag fields that are replaced with relevant information. Known fields are:

- version: The new version
- message: The new commit message
- date: Today's date formatted according to `tokens/date/format` in the config
- version_date: Today's date formatted according to `tokens/version_date/format` in the config
- hash: The new commit hash, full length
- hash4: The new commit hash, first four characters
- hash7: The new commit hash, first seven characters
- hash8: The new commit hash, first eight characters
- author_name: The author name from the git config
- author_email: The author email from the git config

# Updating files

versup can update versions in files. The way this works is by configuring a regex
for each file that you want to update. So for example:

```
"files": {
    "README.rst": [
      ["Version ([\\d\\.]+) ", "Version [version] "],
      ["Version is ([\\d\\.]+)", "Version is [version]"]
    ]
  },
```

Here the file `README.rst` is updated by matching a regex `Version ([\\d\\.]+)`
which will match any text like `Version 1.3` or `Version 1.3.7`. They are standard
regular expressions. The text that is matched is then replaced with the next argument
`Version [version]` where `[version]` is the new version. You can regex and replace on
anything really.

The supported increments are those supported by [Python Semver](https://python-semver.readthedocs.io/en/latest/usage.html#raising-parts-of-a-version)

- major
- minor
- patch
- prerelease
- build

# Scripts

There are a number of pre and post scripts that can be executed at various
stages of the bump process. These are under the `scripts` section. They are
called as-is and receive the new version number as the only argument. They
can be anything, shell scripts, python scripts, etc, but they must be
executable in a regular shell, as they will be invoked as such.

Full Read The Docs can be found at [https://versup.readthedocs.io](https://versup.readthedocs.io)
