"""URLs and HTTP operations provided by the ``main`` app.

This table summarizes what URLs are available for use and what types of HTTP
requests can be accepted by each. Details about each URL, including arguments,
are given after the table.

================== ======== ====== ======== ========
URL                POST     GET    PUT      DELETE
                   (create) (read) (update) (delete)
================== ======== ====== ======== ========
``/``                       *
``gurps-manager/``          *
================== ======== ====== ======== ========

``/``
    ``GET`` requests return a redirect to ``GET gurps-manager/``.

``gurps-manager/``
    ``GET`` requests are forwarded to the ``gurps_manager`` django app. See
    module ``gurps_manager.urls`` for details on what URLs it handles.

"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns( # pylint: disable=C0103
    '',
    url(r'^$', 'main.views.index'),
    url(r'^gurps-manager/', include('gurps_manager.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
