versup
======

MIT license

** Still in early stages, so use with caution **

Bump your project version, update version numbers in your files, create a changelog,
make a commit, and tag it, all in one easy step. versup is also quite configurable.

Install
=======

Install with either poetry

`poetry install`

or pip

`pip install .`

Quick start
===========

To get started all versup needs to know is the new version increment or number.
You can provide it with a valid semantic version increase such as `patch`, `minor`,
`major` etc, or an entirely new semantic version like `1.2.5`.

If you specifiy a version number, then versup will take that version and apply
it to the current project as is. If you provide an increment, it will get the
last version number from either the latest git tag that has a valid version,
or from the default version in the config file.

