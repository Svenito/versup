.. _developer-pages:

Contributing to Versup
======================

If you would like to contribute to Versup by fixing bugs, adding new features, or
updating the documentation, pull requests are welcomed.

In order for your pull request to be accepted there are a few things to note:

* New features and patches must have updated tests added
* The test suite must pass
* Code must be formatted with Black

Currently the Black formatter does not run for Python 2 tests as it's not available.
Once Python 2 is fully end of life, support for Python 2 will be removed.