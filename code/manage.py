#!/usr/bin/env python
"""A command-line utility for project-specific administrative tasks.

From the `official docs`_:

    ``manage.py`` is automatically created in each Django project. ``manage.py``
    is a thin wrapper around ``django-admin.py`` that takes care of two things
    for you before delegating to ``django-admin.py``:

    * It puts your project's package on sys.path.
    * It sets the ``DJANGO_SETTINGS_MODULE`` environment variable so that it
      points to your project's ``settings.py`` file.

See the README for examples of what ``manage.py`` can be used for.

.. _official docs: https://docs.djangoproject.com/en/dev/ref/django-admin/

"""
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
