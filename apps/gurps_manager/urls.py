"""URLs and HTTP operations provided by the ``gurps_manager`` app.

This table summarizes what URLs are available for use and what types of HTTP
requests can be accepted by each. See ``views.py`` for details about the
functions that handle these URLs.

============================================== ======== ====== ======== ========
URL                                            POST     GET    PUT      DELETE
                                               (create) (read) (update) (delete)
============================================== ======== ====== ======== ========
``/``                                                   *
``login/``                                     *        *               *
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
``character/<id>/skills/``                              *
``character/<id>/spells/``                              *
``character/<id>/possessions/``                         *
``character/<id>/traits/``                              *
``character/<id>/hit-locations/``                       *
``character/<id>/skills/update-form/``         *        *
``character/<id>/spells/update-form/``         *        *
``character/<id>/possessions/update-form/``    *        *
``character/<id>/traits/update-form/``         *        *
``character/<id>/hit-locations/update-form/``  *        *
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
from django.contrib.auth.decorators import login_required
from gurps_manager import views

# WARNING! URL names must be unique in all django apps. If any URLs have the
# same name, the reverse() function will produce undefined results. See:
# https://docs.djangoproject.com/en/dev/topics/http/urls/#naming-url-patterns

# pylint: disable=E1120
urlpatterns = patterns( # pylint: disable=C0103
    '',
    url(
        r'^$',
        login_required(views.Index.as_view()),
        name='gurps-manager-index'
    ),
    url(r'^login/$', views.Login.as_view(), name='gurps-manager-login'),

    # campaign-related paths
    url(
        r'^campaign/$',
        login_required(views.Campaign.as_view()),
        name='gurps-manager-campaign'
    ),
    url(
        r'^campaign/create-form/$',
        login_required(views.CampaignCreateForm.as_view()),
        name='gurps-manager-campaign-create-form'
    ),
    url(
        r'^campaign/(\d+)/$',
        login_required(views.CampaignId.as_view()),
        name='gurps-manager-campaign-id',
    ),
    url(
        r'^campaign/(\d+)/update-form/$',
        login_required(views.CampaignIdUpdateForm.as_view()),
        name='gurps-manager-campaign-id-update-form',
    ),
    url(
        r'^campaign/(\d+)/delete-form/$',
        login_required(views.CampaignIdDeleteForm.as_view()),
        name='gurps-manager-campaign-id-delete-form',
    ),

    # character-related paths
    url(
        r'^character/$',
        login_required(views.Character.as_view()),
        name='gurps-manager-character'
    ),
    url(
        r'^character/create-form/$',
        login_required(views.CharacterCreateForm.as_view()),
        name='gurps-manager-character-create-form'
    ),
    url(
        r'^character/(\d+)/$',
        login_required(views.CharacterId.as_view()),
        name='gurps-manager-character-id',
    ),
    url(
        r'^character/(\d+)/update-form/$',
        login_required(views.CharacterIdUpdateForm.as_view()),
        name='gurps-manager-character-id-update-form',
    ),
    url(
        r'^character/(\d+)/delete-form/$',
        login_required(views.CharacterIdDeleteForm.as_view()),
        name='gurps-manager-character-id-delete-form',
    ),
    url(
        r'^character/(\d+)/skills/$',
        login_required(views.CharacterSkills.as_view()),
        name='gurps-manager-character-id-skills',
    ),
    url(
        r'^character/(\d+)/skills/update-form/$',
        login_required(views.CharacterSkillsUpdateForm.as_view()),
        name='gurps-manager-character-id-skills-update-form',
    ),
    url(
        r'^character/(\d+)/spells/$',
        login_required(views.CharacterSpells.as_view()),
        name='gurps-manager-character-id-spells',
    ),
    url(
        r'^character/(\d+)/spells/update-form/$',
        login_required(views.CharacterSpellsUpdateForm.as_view()),
        name='gurps-manager-character-id-spells-update-form',
    ),
    url(
        r'^character/(\d+)/possessions/$',
        login_required(views.Possessions.as_view()),
        name='gurps-manager-character-id-possessions',
    ),
    url(
        r'^character/(\d+)/possessions/update-form/$',
        login_required(views.PossessionsUpdateForm.as_view()),
        name='gurps-manager-character-id-possessions-update-form',
    ),
    url(
        r'^character/(\d+)/traits/$',
        login_required(views.Traits.as_view()),
        name='gurps-manager-character-id-traits',
    ),
    url(
        r'^character/(\d+)/traits/update-form/$',
        login_required(views.TraitsUpdateForm.as_view()),
        name='gurps-manager-character-id-traits-update-form',
    ),
    url(
        r'^character/(\d+)/hit-locations/$',
        login_required(views.HitLocations.as_view()),
        name='gurps-manager-character-id-hit-locations',
    ),
    url(
        r'^character/(\d+)/hit-locations/update-form/$',
        login_required(views.HitLocationsUpdateForm.as_view()),
        name='gurps-manager-character-id-hit-locations-update-form',
    ),
)
