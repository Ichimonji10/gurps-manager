gurps-manager
=============

This repository contains the source code for the GURPS campaign management
system. You can get the full source code at
https://github.com/Ichimonji10/gurps-manager.git. gurps-manager is written using
the Django web app framework. For more on Django, read the excellent `Django
documentation`_.

Deployment Guide
================

This project is not dependent upon any particular web server, app server,
communication protocol, or database backend. However, it is only tested with
certain configurations. Directions for two simple deployments are listed below.

All of the setups listed below require several common pieces of software.
Install the following:

* django-extensions
* django (version 1.6)
* python
* python-django-tables2
* python-factory_boy

When following these deployment guides, you will be instructed to perform
actions at the command line. It is assumed that your command-line client's
current working directory is the root directory if this repository.

Development Setup
-----------------

This setup is easy to accomplish. It is suitable for development work, but it
should __not__ be used in a production environment.

You do not need to install any additional software for this setup.

Initialize the SQLite database::

    $ apps/manage.py syncdb

Start the server that ships with Django::

    $ apps/manage.py runserver

Direct your web browser to http://localhost:8000/. That's it!

Production Setup
----------------

This setup is harder to accomplish. It is suitable for a small production
environment.

Install the following additional software:

* lighttpd
* mysql
* python-flup

TODO: flesh out this section

Documentation
=============

This file (``README.rst``) is written in reStructuredText format. It can be
compiled to several other formats. To compile it to HTML::

    $ rst2html README.rst > README.html

You can generate documentation about the source code itself using epydoc. For
example::

    $ epydoc \
        --config configs/epydocrc \
        --output <output_dir> \
        $(find apps/ -type f -name '*.py')

graphviz must be installed for epydoc to generate graphs.

You can generate a diagram of the database models::

    $ ./manage.py graph_models gurps_manager > gurps_manager.dot
    $ dot -Tsvg -o gurps_manager.svg gurps_manager.dot

Again, graphviz must be installed to generate images.

Static Analysis
===============

You can perform static analysis of individual python files using pylint. Pylint
searches through python code, looking for errors and design issues. To perform
an analysis on the file ``apps/gurps_manager/views.py`` with the following
command::

    $ pylint \
        --init-hook='import sys; sys.path.append("apps/")' \
        apps/gurps_manager/views.py | less

Some warnings are spurious, and you can force pylint to ignore those warnings.
For example, the following might be placed in a models.py file::

    # pylint: disable=R0903
    # "Too few public methods (0/2)"
    # It is both common and OK for a model to have no methods.
    #
    # pylint: disable=W0232
    # "Class has no __init__ method"
    # It is both common and OK for a model to have no __init__ method.

The location of ``pylint: disable=XXXX`` directives is important! For example,
if a "disable" statement is placed at the end of a line, the specified warning
is disabled for only that one line, but if the statement is placed at the top of
a file, the specified warning is ignored throughout that entire file. Don't
apply a "disable" statement to an excessively large scope!

Repository Layout
=================

This section isn't requred reading, but if you really want to understand why the
project is laid out as it is, read on.

TODO: flesh out this section

.. _Django documentation: https://docs.djangoproject.com/en/dev/
