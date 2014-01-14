gurps-manager
=============

This repository contains the source code for the GURPS campaign management
system. You can get the full source code at
https://github.com/Ichimonji10/gurps-manager.git. gurps-manager is written using
the Django web app framework. For more on Django, read the excellent `Django
documentation`_.

This document contains commands that should be run from a shell (command line).
Your shell's current working directory should be the root directory of this
repository. That is, you should ``cd`` to the directory containing this
document.

Deployment Guide
================

This project is not dependent upon any particular web server, app server,
communication protocol, or database backend. However, it is only tested with
certain configurations. Directions for two simple deployments are listed below.

All of the setups listed below require several common pieces of software.
Install the following:

* django (version 1.6)
* python-django-extensions
* python-django-tables2
* python-factory_boy
* python (version 3)

Development Setup
-----------------

This setup is easy to accomplish. It is suitable for development work, but it
should *not* be used in a production environment.

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

Prerequisites
~~~~~~~~~~~~~

Install the following additional software:

* lighttpd
* mysql
* python-gunicorn

Web Server
~~~~~~~~~~

Back up your current lighttpd config files. Then, customize and install new
config files::

    # cp /etc/lighttpd/ /etc/lighttpd.old/
    $ vi configs/lighttpd.conf
    $ vi configs/proxy.conf
    # cp -t /etc/lighttpd/ configs/lighttpd.conf configs/proxy.conf
    # systemctl start lighttpd

The lighttpd config files make several important assumtions. For example, they
make assumptions about where the repository has been cloned to (``/srv/http/``)
and which user the web server should run as. Look them over carefully before
installing them.

At this point, the web server should be capable of serving up static files. This
is despite the fact that the django application is not yet working. To determine
whether lighttpd is working, create a file in the ``static`` directory, and
attempt to fetch it::

    $ echo foo > static/testfile
    $ curl localhost/static/testfile
    $ rm static/testfile

This command causes lighttpd to serve a static file directly from the
``static/`` folder. If you can fetch this static file, then lighttpd is working.

Database
~~~~~~~~

Edit the ``DATABASES`` section of ``apps/main/settings.py``. When you're done,
it will look something like this::

    DATABASES = {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'gurps-manager',
            'USER': 'gurps-manager',
            'PASSWORD': 'hackme',
            'HOST': '127.0.0.1',
            'PORT': '',
        }
    }

Install `MySQL-Python`_, then configure the MySQL database::

    $ mysql -p -u root
    mysql> create database gurps-manager character set utf8;
    mysql> create user 'gurps-manager'@'localhost' IDENTIFIED BY 'hackme';
    mysql> GRANT AlL PRIVILEGES ON gurps-manager.* TO 'gurps-manager'@'localhost';
    mysql> commit;
    mysql> exit

Initialize the database backend::

    $ apps/manage.py syncdb

This will create all necessary tables in the database.

Application
~~~~~~~~~~~

Generate static files::

    $ apps/manage.py collectstatic

This will search each app in the ``apps`` folder for static resources, such as
CSS files and images, and place those files in the ``static/`` folder.

Start the app server (tweak to taste)::

    $ cd apps/
    $ gunicorn main.wsgi:application

Direct your web browser to http://localhost/. That's it!

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

    $ apps/manage.py graph_models gurps_manager > gurps_manager.dot
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
