"""URLs and HTTP operations provided by the ``gurps_manager`` app.

This table summarizes what URLs are available for use and what types of HTTP
requests can be accepted by each. See ``views.py`` for details about the
functions that handle these URLs.

============================================== ======== ====== ======== ========
URL                                            POST     GET    PUT      DELETE
                                               (create) (read) (update) (delete)
============================================== ======== ====== ======== ========
``/``                                                   *
============================================== ======== ====== ======== ========

Web browsers only support ``POST`` and ``GET`` operations; ``PUT`` and
``DELETE`` operations cannot be performed. To accomodate this limitation, a
hidden form field named "_method" is present in forms. For example:

    <input type="hidden" name="_method" value="PUT" />

Thus, none of the URLs listed above actually supports ``PUT`` or ``DELETE``
operations. Support is faked with clever ``POST`` operations.

Theory
======

Most of the URLs in this application are organized in a typical RESTful manner.
This means that a URL consists soley of nouns. For example,
``/character/15/delete/`` is an invalid URL, as "delete" is not a noun. However,
it is OK to send an HTTP DELETE message to ``/character/15/``.

Being RESTful also means that URLs are decomposable.  If
``/character/15/update-form/`` is available, then ``/character/15/``,
``/character/``, and ``/`` should also be available.

There is much to the RESTful design philosophy beyond these few points, and the
curious are encouraged to do some research.

"""
from django.conf.urls import patterns, include, url

urlpatterns = patterns( # pylint: disable=C0103
    'gurps_manager.views',
    url(r'^$', 'index'),
)
