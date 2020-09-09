.. Versup documentation master file, created by
   sphinx-quickstart on Tue Apr  7 10:44:55 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Versup documentation
====================

Versup automates versioning up a project by creating a commit, tagging the release,
creating a changelog, and updating the version across files. Of course, this is all
configurable.

Quickstart
==========

All versup needs is the increment or new version number. If you just want to increase
the semantic version you can invoke it with

.. code:: bash

   versup minor

or if you want to specify the version with

.. code:: bash

   versup 1.72.3

If you specifiy a version number, then versup will take that version and apply
it to the current project as is. If you provide an increment, it will get the
last version number from either the latest git tag that has a valid version,
or from the default version in the config file.

Configuration
=============

One intial launch, versup copies a default config to your home directory (`~/.config/versup.json`) which has some good defaults.

.. code:: python

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
         "posttag": ""  # Script to execute after tagging
      },
   }

You can edit this file to affect all bumps, or create a `.versup.json` file in your project root
and versup will use these values to override the global ones.

Template tags
=============

In various places you can define what text to use for commit messages, or tags etc.
These support tag fields that are replaced with information. Know fields are:

- [version]: The new version
- [message]: The new commit message
- [date]: Today's date formatted according to `tokens/date/format` in the config
- [version_date]: Today's date formatted according to `tokens/version_date/format` in the config
- [hash]: The new commit hash, full length
- [hash4]: The new commit hash, first four characters
- [hash7]: The new commit hash, first seven characters
- [hash8]: The new commit hash, first eight characters
- [author_name]: The author name from the git config
- [author_email]: The author email from the git config

Updating files
==============

versup can update versions in files. The way this works is by configuring a regex
for each file that you want to update. So for example:

.. code::

   "files": {
      "README.rst": [
         ["Version ([\\d\\.]+) ", "Version [version] "],
         ["Version is ([\\d\\.]+)", "Version is [version]"]
      ]
   }


Here the file `README.rst` is updated by matching a regex `Version ([\\d\\.]+)`
which will match any text like `Version 1.3` or `Version 1.3.7`. They are standard
regular expressions. The text that is matched is then replaced with the next argument
`Version [version]` where `[version]` is the new version. You can regex and replace on
anything really.

Scriptsdeveloper-pages pre and post scripts that can be executed at various
stages of the bump process. These are under the `scripts` section. They are
called as-is and receive the new version number as the only argument. They
can be anything, shell scripts, python scripts, etc, but they must be
executable in a regular shell, as they will be invoked as such.


Commandline options
===================

Versup has two command line options

.. code::

   Options:
   --version   Show the version and exit.
   -h, --help  Show this message and exit.

And the following Commands

.. code::

   increment/version  Increment or set project version
   show-config Show the config to be used for the next version updated

The `increment` or `version` command has the following options

.. code::

   --no-commit     Skip making commit
   --no-changelog  Skip changelog update
   --no-tag        Skip creating tag
   -n, --dryrun    Show what will be done but don't apply anything

The `show-config` command accepts these options

.. code:: bash

   -l, --local Show the local configuration options
   -g, --global Show the global configuration options

Contributing to Versup
======================

If you'd like to contribute to Versup please read the :ref:`developer-pages` guide

Indices and tables
==================

* :ref:`modindex`
* :ref:`search`


.. toctree::
   :maxdepth: 2
   :caption: Contents:



