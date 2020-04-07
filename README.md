# versup

MIT license

** Still in early stages, so use with caution **

Bump your project version, update version numbers in your files, create a changelog,
make a commit, and tag it, all in one easy step. versup is also quite configurable.

# Install

Install with either poetry

`poetry install`

or pip

`pip install .`

# Quick start

To get started all versup needs to know is the new version increment or number.
You can provide it with a valid semantic version increase such as `patch`, `minor`,
`major` etc, or an entirely new semantic version like `1.2.5`.

If you specifiy a version number, then versup will take that version and apply
it to the current project as is. If you provide an increment, it will get the
last version number from either the latest git tag that has a valid version,
or from the default version in the config file.

# Configuration

One intial launch, versup copies a default config to your home directory (`~/.config/versup.json`) which has some good defaults.

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
            "premajor",
            "preminor",
            "prepatch",
            "prerelease",
            "custom",
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
    },
    "tag": {
        "enabled": True,  # Tag the bump commit
        "name": "v[version]",  # Template for the name of the tag
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
        "prerelease": "",  # Script to execute before releasing
        "postrelease": "",  # Script to execute after releasing
    },
}
```

You can edit this file to affect all bumps, or create a `.versup.json` file in your project root
and versup will use these values to override the global ones.

# Template tags

In various places you can define what text to use for commit messages, or tags etc.
These support tag fields that are replaced with information. Know fields are:

- version: The new version
- message: The new commit message
- date: Today's date formatted according to `tokens/date/format` in the config
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

# Scripts

There are a number of pre and post scripts that can be executed at various
stages of the bump process. These are under the `scripts` section. They are
called as-is and receive the new version number as the only argument. They
can be anything, shell scripts, python scripts, etc, but they must be
executable in a regular shell, as they will be invoked as such.
