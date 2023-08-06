.. _lfdocs-conf-install:

Install Guide
=============

Follow these steps to install lfdocs-conf:

#. Add ``lfdocs-conf`` to your requirements.txt
#. Create the docs directory in the root of your repo
#. Create docs/conf.py with the following contents::

     from docs_conf.conf import *

   .. note::

      This is the minimal configuration for this file. Further documentation on
      conf.py in :ref:`Configuration Documentation <lfdocs-conf-config>`.

#. Create docs/conf.yaml with the following contents::

     project_cfg: PROJECT

   Replace PROJECT with the name of a project configuration for your top-level
   project. Eg. acumos, onap, opendaylight, opnfv, etc... See here for a `list
   of valid projects
   <https://github.com/lfit/releng-docs-conf/tree/master/docs_conf/defaults>`_.
   If you are a new project and do not yet have a defaults file then please
   propose a patch to the `docs-conf
   <https://gerrit.linuxfoundation.org/infra/#/admin/projects/releng/docs-conf>`_
   project.

   .. note::

      This is the minimal configuration necessary to get this going
      further documentation on conf.yaml is available in the
      :ref:`Configuration Documentation <lfdocs-conf-config>`.

#. Create docs/index.rst with the following contents::

     .. _my-project:

     My Project
     ==========

     Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
     tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim
     veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
     commodo consequat. Duis aute irure dolor in reprehenderit in voluptate
     velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat
     cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id
     est laborum.


   Replace "my-project" and "My Project" with the name of your
   project.

   The first line ".. _my-project:" is a special Sphinx `cross-ref
   <https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html#ref-role>`_
   which is useful to allow other projects to link to arbitrary locations in
   your project. Create these for every section heading in your project to
   ensure that others can link to your project.

   .. note::

      This is the minimal configuration to get a docs page generated for your
      project. What you do from here is entirely up to you. Please refer to the
      `Sphinx reStructuredText Primer
      <http://www.sphinx-doc.org/en/stable/rest.html>`_.

#. (Optional) Copy project logo to docs/_static/logo.png

   .. note::

      The logo should be a small 64x64 png image.

#. (Optional) Copy a favicon to docs/_static/favicon.ico
#. Create a tox.ini with the following contents::

     [tox]
     minversion = 1.6
     envlist =
         docs
         docs-linkcheck
     skipsdist = true

     [testenv:docs]
     deps = -rrequirements.txt
     commands =
         sphinx-build -W -b html -n -d {envtmpdir}/doctrees ./docs/ {toxinidir}/docs/_build/html

     [testenv:docs-linkcheck]
         deps = -rrequirements.txt
         commands = sphinx-build -W -b linkcheck -d {envtmpdir}/doctrees ./docs/ {toxinidir}/docs/_build/linkcheck

   This will configure 2 tox testenvs. The first to generate the docs and the
   2nd to verify links inside of the documentation. The 2nd one is useful to
   ensure the documentation does not contain any broken links.

   .. note::

      The ``-W`` flag enables an option to fail the build even on warnings.
      This flag catches useful issues with docs and projects should strive
      to have their docs passing with this enabled. If setting up an existing
      project that has warnings that are unable to resolve now then
      remove this option temporarily, until such a time that the project can
      clean up the docs.

#. To test run::

     tox -e docs
     google-chrome-stable docs/_build/html/index.html

   .. note::

      Replace the last command with your favourite web browser to view a
      the generated docs.
