.. _lfdocs-conf-config:

Configuration
=============

lfdocs-conf reads aggregates configurations from sources to determine the
effective configuration to build Sphinx. Precedence for configuration
is as follows:

#. project/conf.py
#. project/conf.yaml
#. docs_conf/defaults/{project_cfg}.yaml
#. docs_conf/defaults/default.yaml
#. docs_conf/__init__.py

Typically {project_cfg}.yaml provides a common theme across related
projects. For example all subprojects within the OpenDaylight project share
the common docs_conf/defaults/opendaylight.yaml. All fields provided by
defaults are overidable via one of 2 ways.

#. conf.yaml (preferred)
#. conf.py

.. _lfdocs-conf-conf.yaml:

conf.yaml
---------

In most cases projects should use conf.yaml to configure settings. This file
should at least configure the "project_cfg" setting which will pull the
appropriate defaults configuration for their top level project to ensure a
consistent theme across all subprojects within a project. Settings here can
override settings that you would like different from the project defaults.

Commonly used fields are "project", "version", and "author".

.. literalinclude:: ../examples/conf.yaml
   :language: yaml

.. _lfdocs-conf-conf.py:

conf.py
-------

If conf.yaml does not support a Sphinx configuration you need or you have more
complex configuration needs where Python code might be useful then you can use
conf.py. This file supports the full configuration of `Sphinx conf.py
<http://www.sphinx-doc.org/en/stable/config.html>`_.
