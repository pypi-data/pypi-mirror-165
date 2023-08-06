=======================
FemtoAPI Python Wrapper
=======================

Contents
========

This project contains a Python wrapper for calling the `Femto API`_ functions
of MESc software and additional utilities for handling the data obtained from
the API.
These are bundled in the ``femtoapiwrap`` package that gets installed using
basic setup.

For sample implementations for basic use cases, see the scripts in folder
``examples/basic``.

Modules (it's enough to import ``femtoapiwrap`` only):

* ``femtoapiwrap.api``: the low-level API functions
* ``femtoapiwrap.hi``: high-level types and methods
* ``femtoapiwrap.utils``: miscellaneous functions
* ``femtoapiwrap.errors``: custom exceptions

.. _`Femto API`: https://femtonics.atlassian.net/wiki/spaces/API2

Install
=======

Basic Setup
-----------

.. code:: console

    $ cd <project-root>
    $ pip install -U .

Checking version:

.. code:: python

    import femtoapiwrap
    print(femtoapiwrap.__version__)

Running Examples
----------------

Examples require additional dependencies, which can be installed like this:

.. code:: console

    $ pip install -U .[examples]

Generating Documentation
------------------------

.. code:: console

    $ cd <project-root>
    $ pip install -U .[doc]
    $ cd doc
    $ make clean
    $ make html

Then you can find the documentation at ``<project-root>/doc/_build/index.html``.
Rebuilding often requires the deletion of ``<project-root>/doc/parts/stubs`` too.

Running Tests
-------------

Run tests with coverage report:

.. code:: console

    $ cd <project-root>
    $ pip install .[test]
    $ cd <project-root>/tests
    $ coverage run --source femtoapiwrap -m unittest discover && coverage report

Some test cases need an accessible microscope or a running measurement.
By default, these are skipped and can be activated by setting ``1`` to the
environment variables ``FEMTOAPIWRAP_TEST_MICROSCOPE`` or ``FEMTOAPIWRAP_TEST_ONLINE``
respectively.

Purchase
========

To purchase FemtoAPI please contact `sales@femtonics.eu <sales@femtonics.eu>`_.

Disclaimer
==========

IN NO EVENT SHALL FEMTONICS BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF THE
USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF FEMTONICS HAS BEEN ADVISED
OF THE POSSIBILITY OF SUCH DAMAGE.

FEMTONICS SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
THE SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED HEREUNDER IS
PROVIDED "AS IS". FEMTONICS HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT,
UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
