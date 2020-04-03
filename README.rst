BUMPER
======

Bump your project version, update version numbers in your files, create a changelog,
make a commit, and tag it, all in one easy step. Bumper is also quite configurable.

Quick start
===========

To get started all bumper needs to know is the new version increment or number.
You can provide it with a valid semantic version increase such as `patch`, `minor`,
`major` etc, or an entirely new semantic version like `1.2.5`.

If you specifiy a version number, then bumper will take that version and apply
it to the current project as is. If you provide an increment, it will get the
last version number from either the latest git tag that has a valid version,
or from the default version in the config file.
