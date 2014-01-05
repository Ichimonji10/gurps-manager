"""URLs and HTTP operations provided by the ``gurps_manager`` app."""
from django.conf.urls import patterns, include, url

urlpatterns = patterns( # pylint: disable=C0103
    'gurps_manager.views',
    url(r'^$', 'index'),
)
