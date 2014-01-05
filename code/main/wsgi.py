"""WSGI config for this Django project.

This module contains a WSGI application that can be used by Python application
servers, such as Django's development server or Apache's ``mod_wsgi`` module.
Like any good WSGI application, it exposes a module-level variable named
``application``. The location of this module-level variable is specified in
``settings.py`` via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
from django.core.wsgi import get_wsgi_application
import os

# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
# os.environ["DJANGO_SETTINGS_MODULE"] = "main.settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
application = get_wsgi_application() # pylint: disable=C0103
