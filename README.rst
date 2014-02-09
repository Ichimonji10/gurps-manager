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

Before proceeding, you'll need to install Python 3 and the following Python
modules:

* django (version 1.6)
* django-extensions
* django-tables2
* factory_boy
* pylint

These modules can be installed via any of the usual methods: your package
manager, manually, or with a pypi helper such as easy_install or pip. If you
have virtualenv and pip installed, you can also use a convenience script::

    $ virtualenv-setup.sh <destination_directory>

This creates a virtualenv environment in ``destination_directory``. The
environment can be activated and deactivated like so::

    $ source <destination_directory>/GURPS-ENV/bin/activate
    $ deactivate

You'll also need to edit the file ``apps/main/settings.py`` and provide a value
for the ``SECRET_KEY`` variable. A default value `cannot be provided`_.

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

* gunicorn
* lighttpd
* mysql
* mysql-python

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

Configure the MySQL database::

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

    $ apps/manage.py graph_models gurps_manager | dot -Tsvg -o gurps_manager.svg

Again, graphviz must be installed to generate images.

Static Analysis
===============

You can perform static analysis of individual python files using pylint. Pylint
searches through python code, looking for errors and design issues. You can perform
an analysis on the file ``apps/gurps_manager/views.py`` with the following
command::

    $ pylint \
        --init-hook='import sys; sys.path.append("apps/")' \
        apps/gurps_manager/views.py | less

Alternatively, you can call pylint on all the .py files in the application using
the automated linter which can be called as such:

    $ apps/manage.py linter

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

apps/
-----

This directory contains django apps. Roughly speaking, a django app is a body of
code that can be installed or removed independently of other django apps.

apps/main/
----------

The "main" app contains project-wide settings. It also contains the root URL
dispatcher. To see where requests are dispatched to, read module
``apps.main.urls``.

apps/gurps_manager/
-------------------

The "gurps_manager" app contains everythin necessary for implementing the GURPS
Manager lending system. It contains database models for tracking character
statistics, inventory and other facts; it provides rules for manipulating those
facts; and it provides a user interface for doing so.

There's one layout quirk of special note. The ``templates`` and ``static``
directories contain yet another directory called ``gurps_manager``. It looks
something like this::

    $ tree apps/gurps_manager/
    apps/gurps_manager/
    |-- __init__.py
    |-- models.py
    |-- static
    |   `-- gurps_manager
    |       `-- base.css
    |-- templates
    |   `-- gurps_manager
    |       `-- base.html
    |-- tests.py
    |-- urls.py
    `-- views.py

At first glance, this appears redundant. Why not do the following instead? ::

    $ tree apps/gurps_manager/
    apps/gurps_manager/
    |-- __init__.py
    |-- models.py
    |-- static
    |   `-- base.css
    |-- templates
    |   `-- base.html
    |-- tests.py
    |-- urls.py
    `-- views.py

The latter is a bad idea.

    Now we might be able to get away with putting our templates directly in
    polls/templates (rather than creating another polls subdirectory), but it
    would actually be a bad idea. Django will choose the first template it finds
    whose name matches, and if you had a template with the same name in a
    different application, Django would be unable to distinguish between them.
    We need to be able to point Django at the right one, and the easiest way to
    ensure this is by namespacing them. That is, by putting those templates
    inside another directory named for the application itself.

    -- `Django documentation
    <https://docs.djangoproject.com/en/1.6/intro/tutorial03/#write-views-that-actually-do-something>`__

static
------

The ``static`` folder contains static resources, such as CSS documents or PNG
images. Use the ``collectstatic`` command to populate this directory. The
collectstatic command is described in the `Application`_ section.

Django is good at generating dynamic content, such as HTML documents. However,
it is not good at serving up static files, such as CSS docments or SVG images.
That's the job of a web server, and a web server should serve up resources from
this directory.

The contents of this folder should *not* be version controlled.

configs
-------

Project-wide config files are housed here. Go have a look -- it's pretty
self-explanatory.

sqlite
------

By default, this project uses sqlite as a database backend. This directory
houses that sqlite database file.

The contents of the this folder should *not* be version controlled.

.. _cannot be provided: https://docs.djangoproject.com/en/1.6/ref/settings/#std:setting-SECRET_KEY
.. _Django documentation: https://docs.djangoproject.com/en/dev/
