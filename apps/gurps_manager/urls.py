"""URLs and HTTP operations provided by the ``gurps_manager`` app.

This table summarizes what URLs are available for use and what types of HTTP
requests can be accepted by each. See ``views.py`` for details about the
functions that handle these URLs.

============================================== ======== ====== ======== ========
URL                                            POST     GET    PUT      DELETE
                                               (create) (read) (update) (delete)
============================================== ======== ====== ======== ========
``/``                                                   *
``campaign/``                                  *        *
``campaign/create-form/``                               *
``campaign/<id>/``                                      *      *        *
``campaign/<id>/update-form/``                          *
``campaign/<id>/delete-form/``                          *
``character/``                                 *        *
``character/create-form/``                              *
``character/<id>/``                                     *      *        *
``character/<id>/update-form/``                         *
``character/<id>/delete-form/``                         *
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
from django.conf.urls import patterns, url
from gurps_manager import views

# WARNING! URL names must be unique in all django apps. If any URLs have the
# same name, the reverse() function will produce undefined results. See:
# https://docs.djangoproject.com/en/dev/topics/http/urls/#naming-url-patterns

# pylint: disable=E1120
urlpatterns = patterns( # pylint: disable=C0103
    '',
    url(r'^$', views.Index.as_view(), name='gurps-manager-index'),

    # campaign-related paths
    url(
        r'^campaign/$',
        views.Campaign.as_view(),
        name='gurps-manager-campaign'
    ),
    url(
        r'^campaign/create-form/$',
        views.CampaignCreateForm.as_view(),
        name='gurps-manager-campaign-create-form'
    ),
    url(
        r'^campaign/(\d+)/$',
        views.CampaignId.as_view(),
        name='gurps-manager-campaign-id',
    ),
    url(
        r'^campaign/(\d+)/update-form/$',
        views.CampaignIdUpdateForm.as_view(),
        name='gurps-manager-campaign-id-update-form',
    ),
    url(
        r'^campaign/(\d+)/delete-form/$',
        views.CampaignIdDeleteForm.as_view(),
        name='gurps-manager-campaign-id-delete-form',
    ),

    # character-related paths
    url(
        r'^character/$',
        views.Character.as_view(),
        name='gurps-manager-character'
    ),
    url(
        r'^character/create-form/$',
        views.CharacterCreateForm.as_view(),
        name='gurps-manager-character-create-form'
    ),
    url(
        r'^character/(\d+)/$',
        views.CharacterId.as_view(),
        name='gurps-manager-character-id',
    ),
    url(
        r'^character/(\d+)/update-form/$',
        views.CharacterIdUpdateForm.as_view(),
        name='gurps-manager-character-id-update-form',
    ),
    url(
        r'^character/(\d+)/delete-form/$',
        views.CharacterIdDeleteForm.as_view(),
        name='gurps-manager-character-id-delete-form',
    ),
    url( #TODO update the docstring at the top of the file
        r'^character/(\d+)/skills/update-form/$',
        views.CharacterSkillsUpdateForm.as_view(),
        name='gurps-manager-character-id-skills-update-form',
    ),
)
