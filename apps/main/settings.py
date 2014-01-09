"""Global settings for this Django project.

For a gentle introduction to Django's settings, read `Django settings`_. For a
more thorough reference, read the `settings reference`_. To see the differences
between this settings file and the defaults, run ``manage.py diffsettings``.

This module only contains settings that are Django-specific. If a setting is
listed in the `settings reference`_, it belongs here. Otherwise, it does not
belong here.

.. _settings reference: https://docs.djangoproject.com/en/dev/ref/settings/
.. _Django settings: https://docs.djangoproject.com/en/dev/topics/settings/

"""
import os

# NEVER deploy a site into production with DEBUG turned on!
DEBUG = True
# Display a detailed report for any exception raised during template rendering.
# Django only displays fancy error pages if DEBUG is True, so you'll want to set
# that to take advantage of this setting.
TEMPLATE_DEBUG = DEBUG

LOGIN_URL = 'gurps_manager.views.login'

DATABASES = {
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            '..',
            '..',
            'sqlite',
            'db.db',
        )),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    '..',
    '..',
    'static',
))

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

ROOT_URLCONF = 'main.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'main.wsgi.application'

INSTALLED_APPS = (
    'django_extensions',
    'django_tables2',
    'gurps_manager',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
#
# Logging: http://docs.djangoproject.com/en/dev/topics/logging
# Admins: https://docs.djangoproject.com/en/1.6/ref/settings/#std:setting-ADMINS
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
