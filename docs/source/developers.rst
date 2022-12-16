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

Installing for development
=========================

This is best done via poetry and is as simple as

.. code::

    poetry install

This will create a new environment for versup and install all the dependencies.
In order to make use of the new environment run

.. code::

    poetry shell

which will source the environment.

Running tests
=============

The tests use pytest and coverage. There is a Makefile that bundles the commands
together. All you need to do is run

.. code::

    make test

and the tests will be run and a coverage report printed to the terminal
