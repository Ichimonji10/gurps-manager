"""Unit tests for the ``views`` module.

Each test case  in this module tests a single view. For example,
``CampaignCreateFormTestCase`` tests just the ``campaign_create_form`` view.

"""
from django.core.urlresolvers import reverse
from django.test import TestCase
from gurps_manager import factories, models

# pylint: disable=E1101
# Class 'Campaign' has no 'objects' member (no-member)
# Class 'CampaignFactory' has no '<blah>' member (no-member)
#
# pylint: disable=E1103
# Instance of 'WSGIRequest' has no 'status_code' member
# (but some types could not be inferred) (maybe-no-member)
#
# pylint: disable=R0904
# Classes inheriting from TestCase will have 60+ too many public methods, and
# that's not something I have control over. Ignore it.

class IndexTestCase(TestCase):
    """Tests for the ``/`` path."""
    PATH = reverse('gurps-manager-index')

    def setUp(self):
        """Authenticate the test client."""
        _login(self.client)

    def test_login_required(self):
        """Ensure user must be logged in to GET this URL."""
        _test_login_required(self)

    def test_post(self):
        """POST ``self.PATH``."""
        response = self.client.post(self.PATH)
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.PATH``."""
        response = self.client.get(self.PATH)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """POST ``self.PATH`` and emulate a PUT request."""
        response = self.client.put(self.PATH, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """POST ``self.PATH`` and emulate a DELETE request."""
        response = self.client.delete(self.PATH, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

class LoginTestCase(TestCase):
    """Tests for the ``login/`` path."""
    PATH = reverse('gurps-manager-login')

    def test_post(self):
        """Log in sucessfully."""
        user, password = factories.create_user()
        response = self.client.post(
            self.PATH,
            {'username': user.username, 'password': password}
        )
        self.assertRedirects(response, reverse('gurps-manager-index'))

    def test_post_failure_v1(self):
        """Log in, but do not provide any credentials."""
        response = self.client.post(self.PATH, {})
        self.assertRedirects(response, self.PATH)

    def test_post_failure_v2(self):
        """Log in with an invalid username/password combination."""
        response = self.client.post(
            self.PATH,
            {'username': 'foo', 'password': 'bar'}
        )
        self.assertRedirects(response, self.PATH)

    def test_post_failure_v3(self):
        """Log in with an inactive user."""
        user, password = factories.create_user()
        user.is_active = False
        user.save()
        response = self.client.post(
            self.PATH,
            {'username': user.username, 'password': password}
        )
        self.assertRedirects(response, self.PATH)

    def test_get(self):
        """Get the login page."""
        response = self.client.get(self.PATH)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """POST ``self.PATH`` and emulate a PUT request."""
        response = self.client.put(self.PATH, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """POST ``self.PATH`` ane emulate a DELETE request, thus logging out."""
        _login(self.client)
        response = self.client.post(self.PATH, {'_method': 'DELETE'})
        self.assertRedirects(response, self.PATH)

class CampaignTestCase(TestCase):
    """Tests for the ``campaign/`` path."""
    PATH = reverse('gurps-manager-campaign')

    def setUp(self):
        """Authenticate the test client."""
        self.user = _login(self.client)[0]

    def test_login_required(self):
        """Ensure user must be logged in to GET this URL."""
        _test_login_required(self)

    def test_post(self):
        """POST ``self.PATH``."""
        # A Campaign object contains FKs pointing to other objects. Save those
        # remote objects, and place their IDs in a dict.
        campaign_attrs = factories.CampaignFactory.attributes()
        campaign_attrs['owner'].save()
        campaign_attrs['owner'] = self.user.id

        num_campaigns = models.Campaign.objects.count()
        response = self.client.post(self.PATH, campaign_attrs)
        self.assertEqual(models.Campaign.objects.count(), num_campaigns + 1)
        self.assertRedirects(
            response,
            reverse(
                'gurps-manager-campaign-id',
                args=[models.Campaign.objects.latest('id').id]
            )
        )

    def test_post_failure(self):
        """POST ``self.PATH``, incorrectly."""
        response = self.client.post(self.PATH, {})
        self.assertRedirects(
            response,
            reverse('gurps-manager-campaign-create-form')
        )

    def test_get(self):
        """GET ``self.PATH``."""
        response = self.client.get(self.PATH)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """POST ``self.PATH`` and emulate a PUT request."""
        response = self.client.put(self.PATH, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """POST ``self.PATH`` and emulate a DELETE request."""
        response = self.client.delete(self.PATH, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

class CampaignCreateFormTestCase(TestCase):
    """Tests for the ``campaign/create-form/`` path."""
    PATH = reverse('gurps-manager-campaign-create-form')

    def setUp(self):
        """Authenticate the test client."""
        self.user = _login(self.client)[0]

    def test_login_required(self):
        """Ensure user must be logged in to GET this URL."""
        _test_login_required(self)

    def test_post(self):
        """POST ``self.PATH``."""
        response = self.client.post(self.PATH)
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.PATH``."""
        response = self.client.get(self.PATH)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """POST ``self.PATH`` and emulate a PUT request."""
        response = self.client.put(self.PATH, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """POST ``self.PATH`` and emulate a DELETE request."""
        response = self.client.delete(self.PATH, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

class CampaignIdTestCase(TestCase):
    """Tests for the ``campaign/<id>/`` path."""
    def setUp(self):
        """Create a campaign and set ``self.path``.

        The created campaign is accessible as ``self.campaign``.

        """
        user = _login(self.client)[0]
        self.campaign = factories.CampaignFactory.create(owner=user)
        self.path = reverse(
            'gurps-manager-campaign-id',
            args=[self.campaign.id]
        )

    def test_login_required(self):
        """Ensure user must be logged in to get info about a campaign."""
        _test_login_required(self, self.path)

    def test_post(self):
        """POST ``self.path``."""
        response = self.client.post(self.path)
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """Get info about a campaign."""
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)

    def test_get_bad_id(self):
        """Get info about a non-existent campaign."""
        self.campaign.delete()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 404)

    def test_get_failure(self):
        """Get info about a campaign, without the necessary rights."""
        campaign = factories.CampaignFactory.create()
        response = self.client.get(reverse(
            'gurps-manager-campaign-id',
            args=[campaign.id]
        ))
        self.assertEqual(response.status_code, 403)

    def test_put(self):
        """Update a campaign."""
        data = factories.CampaignFactory.attributes()
        data['owner'].save()
        data['owner'] = self.campaign.owner.id
        data['_method'] = 'PUT'
        response = self.client.post(self.path, data)
        self.assertRedirects(response, self.path)

    def test_put_failure_v1(self):
        """Update a campaign, using invalid data."""
        # A CampaignForm requires more than just a name.
        data = {'_method': 'PUT', 'name': ''}
        response = self.client.post(self.path, data)
        self.assertRedirects(
            response,
            reverse(
                'gurps-manager-campaign-id-update-form',
                args=[self.campaign.id]
            )
        )

    def test_put_failure_v2(self):
        """Update a campaign, without the necessary rights."""
        campaign = factories.CampaignFactory.create()
        response = self.client.post(
            reverse('gurps-manager-campaign-id', args=[campaign.id]),
            {'_method': 'PUT'}
        )
        self.assertEqual(response.status_code, 403)

    def test_delete(self):
        """Delete a campaign."""
        response = self.client.post(self.path, {'_method': 'DELETE'})
        self.assertRedirects(response, reverse('gurps-manager-campaign'))

    def test_delete_failure(self):
        """Delete a campaign, without the necessary rights."""
        campaign = factories.CampaignFactory.create()
        response = self.client.post(
            reverse('gurps-manager-campaign-id', args=[campaign.id]),
            {'_method': 'DELETE'}
        )
        self.assertEqual(response.status_code, 403)


class CampaignIdUpdateFormTestCase(TestCase):
    """Tests for the ``campaign/<id>/update-form/`` path."""
    def setUp(self):
        """Create a campaign and set ``self.path``.

        The created campaign is accessible as ``self.campaign``.

        """
        user = _login(self.client)[0]
        self.campaign = factories.CampaignFactory.create(owner=user)
        self.path = reverse(
            'gurps-manager-campaign-id-update-form',
            args=[self.campaign.id]
        )

    def test_login_required(self):
        """Ensure user must be logged in to GET this URL."""
        _test_login_required(self, self.path)

    def test_post(self):
        """POST ``self.path``."""
        response = self.client.post(self.path)
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """Get a campaign update form."""
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)

    def test_get_bad_id(self):
        """Get a campaign update form for a non-existent campaign."""
        self.campaign.delete()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 404)

    def test_get_failure(self):
        """Get a campaign update form, without the necessary rights."""
        campaign = factories.CampaignFactory.create()
        response = self.client.get(reverse(
            'gurps-manager-campaign-id-update-form',
            args=[campaign.id]
        ))
        self.assertEqual(response.status_code, 403)

    def test_put(self):
        """POST ``self.path`` and emulate a PUT request."""
        response = self.client.put(self.path, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """POST ``self.path`` and emulate a DELETE request."""
        response = self.client.delete(self.path, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

class CampaignIdDeleteFormTestCase(TestCase):
    """Tests for the ``campaign/<id>/delete-form/`` path."""
    def setUp(self):
        """Create a campaign and set ``self.path``.

        The created campaign is accessible as ``self.campaign``.

        """
        user = _login(self.client)[0]
        self.campaign = factories.CampaignFactory.create(owner=user)
        self.path = reverse(
            'gurps-manager-campaign-id-delete-form',
            args=[self.campaign.id]
        )

    def test_login_required(self):
        """Ensure user must be logged in to GET this URL."""
        _test_login_required(self, self.path)

    def test_post(self):
        """POST ``self.path``."""
        response = self.client.post(self.path)
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """Get a campaign deletion form, without the necessary rights."""
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)

    def test_get_bad_id(self):
        """Get a campaign deletion form for a non-existent campaign."""
        self.campaign.delete()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 404)

    def test_get_failure(self):
        """Get a campaign deletion form, without the necessary rights."""
        campaign = factories.CampaignFactory.create()
        response = self.client.get(reverse(
            'gurps-manager-campaign-id-delete-form',
            args=[campaign.id]
        ))
        self.assertEqual(response.status_code, 403)

    def test_put(self):
        """POST ``self.path`` and emulate a PUT request."""
        response = self.client.put(self.path, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """POST ``self.path`` and emulate a DELETE request."""
        response = self.client.delete(self.path, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

class CampaignIdSpellsUpdateFormTestCase(TestCase):
    """Tests for the ``campaign/<id>/spells/update-form/`` path."""
    def setUp(self):
        """Create a campaign and set ``self.path``.

        The created campaign is accessible as ``self.campaign``.

        """
        user = _login(self.client)[0]
        self.campaign = factories.CampaignFactory.create(owner=user)
        self.path = reverse(
            'gurps-manager-campaign-id-spells-update-form',
            args=[self.campaign.id]
        )

    def test_login_required(self):
        """Ensure user must be logged in to GET this URL."""
        _test_login_required(self, self.path)

    def test_post(self):
        """POST ``self.path``."""
        response = self.client.post(self.path)
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.path``."""
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)

    def test_get_bad_id(self):
        """GET ``self.path`` with a bad ID."""
        self.campaign.delete()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 404)

    def test_get_failure(self):
        """Let some other user own ``self.campaign``, then GET ``self.path``.""" # pylint: disable=C0301
        self.campaign.owner = factories.UserFactory.create()
        self.campaign.save()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 403)

    def test_put(self):
        """POST ``self.path`` and emulate a PUT request."""
        response = self.client.put(self.path, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """POST ``self.path`` and emulate a DELETE request."""
        response = self.client.delete(self.path, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

class CampaignIdSpellsTestCase(TestCase):
    """Tests for the ``campaign/<id>/spells/`` path."""
    def setUp(self):
        """Create a campaign and set ``self.path``.

        The created campaign is accessible as ``self.campaign``.

        """
        user = _login(self.client)[0]
        self.campaign = factories.CampaignFactory.create(owner=user)
        self.path = reverse(
            'gurps-manager-campaign-id-spells',
            args=[self.campaign.id]
        )

    def test_login_required(self):
        """Ensure user must be logged in to GET this URL."""
        _test_login_required(self, self.path)

    def test_post(self):
        """Create a spell for a campaign."""
        data = {
            'spell_set-INITIAL_FORMS': ['0'],
            'spell_set-TOTAL_FORMS': ['1'],
            'spell_set-MAX_NUM_FORMS': ['10'],
            'spell_set-0-id': [''], # blank, b/c creating a new spell
            'spell_set-0-campaign': [str(self.campaign.id)],
            'spell_set-0-name': ['Magic Missile'],
            'spell_set-0-school': ['magic 101'],
            'spell_set-0-cast_time': ['10'],
            'spell_set-0-resist': ['1'],
            'spell_set-0-duration': ['2'],
            'spell_set-0-difficulty': ['3'],
            'spell_set-0-initial_fatigue_cost': ['4'],
            'spell_set-0-maintenance_fatigue_cost': ['5'],
        }
        response = self.client.post(self.path, data)
        self.assertRedirects(
            response,
            reverse(
                'gurps-manager-campaign-id-spells',
                args=[self.campaign.id]
            )
        )

    def test_post_failure_v1(self):
        """Create an spell for a non-existent campaign."""
        self.campaign.delete()
        response = self.client.post(self.path, {})
        self.assertEqual(response.status_code, 404)

    def test_post_failure_v2(self):
        """Create an spell for a campaign, but with invalid data."""
        data = {
            'spell_set-INITIAL_FORMS': ['0'],
            'spell_set-TOTAL_FORMS': ['1'],
            'spell_set-MAX_NUM_FORMS': ['10'],
            'spell_set-0-duration': ['-1'],
        }
        response = self.client.post(self.path, data)
        self.assertRedirects(
            response,
            reverse(
                'gurps-manager-campaign-id-spells-update-form',
                args=[self.campaign.id]
            )
        )

    def test_post_failure_v3(self):
        """Create a spell for a campaign, but without rights to do so."""
        path = reverse(
            'gurps-manager-campaign-id-spells',
            args=[factories.CampaignFactory.create().id]
        )
        data = {
            'item_set-INITIAL_FORMS': ['0'],
            'item_set-TOTAL_FORMS': ['1'],
            'item_set-MAX_NUM_FORMS': ['10'],
        }
        response = self.client.post(path, data)
        self.assertEqual(response.status_code, 403)

    def test_get(self):
        """GET ``self.path``."""
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)

    def test_get_bad_id(self):
        """GET ``self.path`` with a bad ID."""
        self.campaign.delete()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 404)

    def test_get_failure(self):
        """Let some other user own ``self.campaign``, then GET ``self.path``.""" # pylint: disable=C0301
        self.campaign.owner = factories.UserFactory.create()
        self.campaign.save()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 403)

    def test_put(self):
        """POST ``self.path`` and emulate a PUT request."""
        response = self.client.put(self.path, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """POST ``self.path`` and emulate a DELETE request."""
        response = self.client.delete(self.path, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

class CampaignIdItemsUpdateFormTestCase(TestCase):
    """Tests for the ``campaign/<id>/items/update-form/`` path."""
    def setUp(self):
        """Create a campaign and set ``self.path``.

        The created campaign is accessible as ``self.campaign``.

        """
        user = _login(self.client)[0]
        self.campaign = factories.CampaignFactory.create(owner=user)
        self.path = reverse(
            'gurps-manager-campaign-id-items-update-form',
            args=[self.campaign.id]
        )

    def test_login_required(self):
        """Ensure user must be logged in to GET this URL."""
        _test_login_required(self, self.path)

    def test_post(self):
        """POST ``self.path``."""
        response = self.client.post(self.path)
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.path``."""
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)

    def test_get_bad_id(self):
        """GET ``self.path`` with a bad ID."""
        self.campaign.delete()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 404)

    def test_get_failure(self):
        """Let some other user own ``self.campaign``, then GET ``self.path``.""" # pylint: disable=C0301
        self.campaign.owner = factories.UserFactory.create()
        self.campaign.save()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 403)

    def test_put(self):
        """POST ``self.path`` and emulate a PUT request."""
        response = self.client.put(self.path, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """POST ``self.path`` and emulate a DELETE request."""
        response = self.client.delete(self.path, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

class CampaignIdItemsTestCase(TestCase):
    """Tests for the ``campaign/<id>/items/`` path."""
    def setUp(self):
        """Create a campaign and set ``self.path``.

        The created campaign is accessible as ``self.campaign``.

        """
        user = _login(self.client)[0]
        self.campaign = factories.CampaignFactory.create(owner=user)
        self.path = reverse(
            'gurps-manager-campaign-id-items',
            args=[self.campaign.id]
        )

    def test_login_required(self):
        """Ensure user must be logged in to GET this URL."""
        _test_login_required(self, self.path)

    def test_post(self):
        """Create an item for a campaign."""
        data = {
            'item_set-INITIAL_FORMS': ['0'],
            'item_set-TOTAL_FORMS': ['1'],
            'item_set-MAX_NUM_FORMS': ['10'],
            'item_set-0-id': [''], # blank, b/c creating new item
            'item_set-0-campaign': [str(self.campaign.id)],
            'item_set-0-name': ['Bladed Pinions'],
            'item_set-0-description': [''],
            'item_set-0-value': ['2.0'],
            'item_set-0-weight': ['3.0'],
        }
        response = self.client.post(self.path, data)
        self.assertRedirects(
            response,
            reverse(
                'gurps-manager-campaign-id-items',
                args=[self.campaign.id]
            )
        )

    def test_post_failure_v1(self):
        """Create an item for a non-existent campaign."""
        self.campaign.delete()
        response = self.client.post(self.path, {})
        self.assertEqual(response.status_code, 404)

    def test_post_failure_v2(self):
        """Create an item for a campaign, but with invalid data."""
        data = {
            'item_set-INITIAL_FORMS': ['0'],
            'item_set-TOTAL_FORMS': ['1'],
            'item_set-MAX_NUM_FORMS': ['10'],
            'item_set-0-weight': ['-1.0'],
        }
        response = self.client.post(self.path, data)
        self.assertRedirects(
            response,
            reverse(
                'gurps-manager-campaign-id-items-update-form',
                args=[self.campaign.id]
            )
        )

    def test_post_failure_v3(self):
        """Create an item for a campaign, but without rights to do so."""
        path = reverse(
            'gurps-manager-campaign-id-items',
            args=[factories.CampaignFactory.create().id]
        )
        data = {
            'item_set-INITIAL_FORMS': ['0'],
            'item_set-TOTAL_FORMS': ['1'],
            'item_set-MAX_NUM_FORMS': ['10'],
        }
        response = self.client.post(path, data)
        self.assertEqual(response.status_code, 403)

    def test_get(self):
        """GET ``self.path``."""
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)

    def test_get_bad_id(self):
        """GET ``self.path`` with a bad ID."""
        self.campaign.delete()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 404)

    def test_get_failure(self):
        """Let some other user own ``self.campaign``, then GET ``self.path``.""" # pylint: disable=C0301
        self.campaign.owner = factories.UserFactory.create()
        self.campaign.save()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 403)

    def test_put(self):
        """POST ``self.path`` and emulate a PUT request."""
        response = self.client.put(self.path, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """POST ``self.path`` and emulate a DELETE request."""
        response = self.client.delete(self.path, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

class CharacterTestCase(TestCase):
    """Tests for the ``character/`` path."""
    PATH = reverse('gurps-manager-character')

    def setUp(self):
        """Authenticate the test client."""
        self.user = _login(self.client)[0]

    def test_login_required(self):
        """Ensure user must be logged in to GET this URL."""
        _test_login_required(self)

    def test_post(self):
        """POST ``self.PATH``."""
        # A Character object contains FKs pointing to other objects. Save those
        # remote objects, and place their IDs in a dict.
        char_attrs = factories.CharacterFactory.attributes()
        char_attrs['campaign'] = factories.CampaignFactory.create().id
        char_attrs['owner'] = self.user.id

        # POSTing to self.PATH should create a new Character object.
        num_characters = models.Character.objects.count()
        response = self.client.post(self.PATH, char_attrs)
        self.assertEqual(models.Character.objects.count(), num_characters + 1)

        # The client should be redirected after successfully POSTing.
        self.assertRedirects(
            response,
            reverse(
                'gurps-manager-character-id',
                args=[models.Character.objects.latest('id').id]
            )
        )

    def test_post_failure(self):
        """POST ``self.PATH``, incorrectly."""
        response = self.client.post(self.PATH, {})
        self.assertRedirects(
            response,
            reverse('gurps-manager-character-create-form')
        )

    def test_get(self):
        """GET ``self.PATH``."""
        response = self.client.get(self.PATH)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """POST ``self.PATH`` and emulate a PUT request."""
        response = self.client.put(self.PATH, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """POST ``self.PATH`` and emulate a DELETE request."""
        response = self.client.delete(self.PATH, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

class CharacterCreateFormTestCase(TestCase):
    """Tests for the ``character/create-form/`` path."""
    PATH = reverse('gurps-manager-character-create-form')

    def setUp(self):
        """Authenticate the test client."""
        _login(self.client)

    def test_login_required(self):
        """Ensure user must be logged in to GET this URL."""
        _test_login_required(self)

    def test_post(self):
        """POST ``self.PATH``."""
        response = self.client.post(self.PATH)
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.PATH``."""
        response = self.client.get(self.PATH)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        """POST ``self.PATH`` and emulate a PUT request."""
        response = self.client.put(self.PATH, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """POST ``self.PATH`` and emulate a DELETE request."""
        response = self.client.delete(self.PATH, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

class CharacterIdTestCase(TestCase):
    """Tests for the ``character/<id>/`` path."""
    def setUp(self):
        """Create a character and set ``self.path``.

        The created character is accessible as ``self.character``, and the test
        user owns the character.

        """
        user = _login(self.client)[0]
        self.character = factories.CharacterFactory.create(owner=user)
        self.path = reverse(
            'gurps-manager-character-id',
            args=[self.character.id]
        )

    def test_login_required(self):
        """Ensure user must be logged in to GET this URL."""
        _test_login_required(self, self.path)

    def test_post(self):
        """POST ``self.path``."""
        response = self.client.post(self.path)
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.path``."""
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)

    def test_get_bad_id(self):
        """GET ``self.path`` with a bad ID."""
        self.character.delete()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 404)

    def test_get_failure(self):
        """Let some other user own ``self.character``, then try to get it."""
        self.character.owner = factories.UserFactory.create()
        self.character.save()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 403)

    def test_put(self):
        """Update ``self.character``."""
        data = factories.CharacterFactory.attributes()
        data['campaign'] = self.character.campaign.id # Make FK attribute sane
        data['owner'] = self.character.owner.id # Make FK attribute sane
        data['_method'] = 'PUT'
        response = self.client.post(self.path, data)
        self.assertRedirects(response, self.path)

    def test_put_failure(self):
        """Update ``self.character``, but use a malformed form."""
        # A CharacterForm requires more than just a name.
        data = {'_method': 'PUT', 'name': ''}
        response = self.client.post(self.path, data)
        self.assertRedirects(
            response,
            reverse(
                'gurps-manager-character-id-update-form',
                args=[self.character.id]
            )
        )

    def test_put_failure_2(self):
        """Let some other user own ``self.character``, then try to update it."""
        self.character.owner = factories.UserFactory.create()
        self.character.save()
        response = self.client.post(self.path, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 403)

    def test_delete(self):
        """Delete ``self.character``."""
        response = self.client.post(self.path, {'_method': 'DELETE'})
        self.assertRedirects(response, reverse('gurps-manager-character'))

    def test_delete_failure(self):
        """Let some other user own ``self.character``, then try to delete it."""
        self.character.owner = factories.UserFactory.create()
        self.character.save()
        response = self.client.post(self.path, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 403)

class CharacterIdUpdateFormTestCase(TestCase):
    """Tests for the ``character/<id>/update-form/`` path."""
    def setUp(self):
        """Create a character and set ``self.path``.

        The created character is accessible as ``self.character``.

        """
        user = _login(self.client)[0]
        self.character = factories.CharacterFactory.create(owner=user)
        self.path = reverse(
            'gurps-manager-character-id-update-form',
            args=[self.character.id]
        )

    def test_login_required(self):
        """Ensure user must be logged in to GET this URL."""
        _test_login_required(self, self.path)

    def test_post(self):
        """POST ``self.path``."""
        response = self.client.post(self.path)
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.path``."""
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)

    def test_get_bad_id(self):
        """GET ``self.path`` with a bad ID."""
        self.character.delete()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 404)

    def test_get_failure(self):
        """Let some other user own ``self.character``, then GET ``self.path``.""" # pylint: disable=C0301
        self.character.owner = factories.UserFactory.create()
        self.character.save()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 403)

    def test_put(self):
        """POST ``self.path`` and emulate a PUT request."""
        response = self.client.put(self.path, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """POST ``self.path`` and emulate a DELETE request."""
        response = self.client.delete(self.path, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

class CharacterIdDeleteFormTestCase(TestCase):
    """Tests for the ``character/<id>/delete-form/`` path."""
    def setUp(self):
        """Create a character and set ``self.path``.

        The created character is accessible as ``self.character``.

        """
        user = _login(self.client)[0]
        self.character = factories.CharacterFactory.create(owner=user)
        self.path = reverse(
            'gurps-manager-character-id-delete-form',
            args=[self.character.id]
        )

    def test_login_required(self):
        """Ensure user must be logged in to GET this URL."""
        _test_login_required(self, self.path)

    def test_post(self):
        """POST ``self.path``."""
        response = self.client.post(self.path)
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.path``."""
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)

    def test_get_bad_id(self):
        """GET ``self.path`` with a bad ID."""
        self.character.delete()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 404)

    def test_get_failure(self):
        """Let some other user own ``self.character``, then GET ``self.path``.""" # pylint: disable=C0301
        self.character.owner = factories.UserFactory.create()
        self.character.save()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 403)

    def test_put(self):
        """POST ``self.path`` and emulate a PUT request."""
        response = self.client.put(self.path, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """POST ``self.path`` and emulate a DELETE request."""
        response = self.client.delete(self.path, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

class CharacterIdSkillsUpdateFormTestCase(TestCase):
    """Tests for the ``character/<id>/skills/update-form/`` path."""
    def setUp(self):
        """Create a character and set ``self.path``.

        The created character is accessible as ``self.character``.

        """
        user = _login(self.client)[0]
        self.character = factories.CharacterFactory.create(owner=user)
        self.path = reverse(
            'gurps-manager-character-id-skills-update-form',
            args=[self.character.id]
        )

    def test_login_required(self):
        """Ensure user must be logged in to GET this URL."""
        _test_login_required(self, self.path)

    def test_post(self):
        """POST ``self.path``."""
        response = self.client.post(self.path)
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.path``."""
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)

    def test_get_bad_id(self):
        """GET ``self.path`` with a bad ID."""
        self.character.delete()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 404)

    def test_get_failure(self):
        """Let some other user own ``self.character``, then GET ``self.path``.""" # pylint: disable=C0301
        self.character.owner = factories.UserFactory.create()
        self.character.save()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 403)

    def test_put(self):
        """POST ``self.path`` and emulate a PUT request."""
        response = self.client.put(self.path, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """POST ``self.path`` and emulate a DELETE request."""
        response = self.client.delete(self.path, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

class CharacterIdSkillsTestCase(TestCase):
    """Tests for the ``character/<id>/skills/`` path."""
    def setUp(self):
        """Create a character and set ``self.path``.

        The created character is accessible as ``self.character``.

        """
        user = _login(self.client)[0]
        self.character = factories.CharacterFactory.create(owner=user)
        self.path = reverse(
            'gurps-manager-character-id-skills',
            args=[self.character.id]
        )

    def test_login_required(self):
        """Ensure user must be logged in to GET this URL."""
        _test_login_required(self, self.path)

    def test_post(self):
        """Update a character's skills."""
        self.character.campaign.skillsets.add(
            models.SkillSet.objects.get(name__exact='Professional')
        )
        data = {
            'characterskill_set-INITIAL_FORMS': ['0'],
            'characterskill_set-TOTAL_FORMS': ['1'],
            'characterskill_set-MAX_NUM_FORMS': ['10'],

            'characterskill_set-0-id': [''],
            'characterskill_set-0-character': [str(self.character.id)],
            'characterskill_set-0-bonus_level': ['0'],
            'characterskill_set-0-comments': [''],
            'characterskill_set-0-points': ['3.0'],
            'characterskill_set-0-skill': [str(
                # This skill belongs to the 'General' skillset.
                models.Skill.objects.get(name__exact='Abacus').id
            )],
        }

        response = self.client.post(self.path, data)
        self.assertRedirects(
            response,
            reverse(
                'gurps-manager-character-id-skills',
                args=[self.character.id]
            )
        )

    def test_post_failure_v1(self):
        """Update a character's skills, but with invalid data."""
        # Management form data must be present, or else an exception is thrown.
        data = {
            'characterskill_set-INITIAL_FORMS': ['0'],
            'characterskill_set-TOTAL_FORMS': ['1'],
            'characterskill_set-MAX_NUM_FORMS': ['10'],
        }
        response = self.client.post(self.path, data)
        self.assertRedirects(
            response,
            reverse(
                'gurps-manager-character-id-skills-update-form',
                args=[self.character.id]
            )
        )

    def test_post_failure_v2(self):
        """Update a character's skills, without the rights to do so."""
        character = factories.CharacterFactory.create()
        path = reverse('gurps-manager-character-id-skills', args=[character.id])
        response = self.client.post(path, {})
        self.assertEqual(response.status_code, 403)

    def test_get(self):
        """GET ``self.path``."""
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)

    def test_get_bad_id(self):
        """GET ``self.path`` with a bad ID."""
        self.character.delete()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 404)

    def test_get_failure(self):
        """Let some other user own ``self.character``, then GET ``self.path``.""" # pylint: disable=C0301
        self.character.owner = factories.UserFactory.create()
        self.character.save()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 403)

    def test_put(self):
        """POST ``self.path`` and emulate a PUT request."""
        response = self.client.put(self.path, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """POST ``self.path`` and emulate a DELETE request."""
        response = self.client.delete(self.path, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

class CharacterIdSpellsUpdateFormTestCase(TestCase):
    """Tests for the ``character/<id>/spells/update-form/`` path."""
    def setUp(self):
        """Create a character and set ``self.path``.

        The created character is accessible as ``self.character``.

        """
        user = _login(self.client)[0]
        self.character = factories.CharacterFactory.create(owner=user)
        self.path = reverse(
            'gurps-manager-character-id-spells-update-form',
            args=[self.character.id]
        )

    def test_login_required(self):
        """Ensure user must be logged in to GET this URL."""
        _test_login_required(self, self.path)

    def test_post(self):
        """POST ``self.path``."""
        response = self.client.post(self.path)
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.path``."""
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)

    def test_get_bad_id(self):
        """GET ``self.path`` with a bad ID."""
        self.character.delete()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 404)

    def test_get_failure(self):
        """Let some other user own ``self.character``, then GET ``self.path``.""" # pylint: disable=C0301
        self.character.owner = factories.UserFactory.create()
        self.character.save()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 403)

    def test_put(self):
        """POST ``self.path`` and emulate a PUT request."""
        response = self.client.put(self.path, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """POST ``self.path`` and emulate a DELETE request."""
        response = self.client.delete(self.path, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

class CharacterIdSpellsTestCase(TestCase):
    """Tests for the ``character/<id>/spells/`` path."""
    def setUp(self):
        """Create a character and set ``self.path``.

        The created character is accessible as ``self.character``.

        """
        user = _login(self.client)[0]
        self.character = factories.CharacterFactory.create(owner=user)
        self.path = reverse(
            'gurps-manager-character-id-spells',
            args=[self.character.id]
        )

    def test_login_required(self):
        """Ensure user must be logged in to GET this URL."""
        _test_login_required(self, self.path)

    def test_post(self):
        """Create a new CharacterSpell object."""
        # Give character access to a skill.
        self.character.campaign.skillsets.add(
            models.SkillSet.objects.get(name__exact='Professional')
        )
        skill = models.Skill.objects.get(name__exact='Abacus')
        # Give character access to a spell.
        spell = factories.SpellFactory.create(campaign=self.character.campaign)
        # Construct form data.
        data = {
            'characterspell_set-INITIAL_FORMS': ['0'],
            'characterspell_set-TOTAL_FORMS': ['1'],
            'characterspell_set-MAX_NUM_FORMS': ['10'],
            'characterspell_set-0-id': [''], # no id, b/c creating a new spell
            'characterspell_set-0-character': [str(self.character.id)],
            'characterspell_set-0-bonus_level': ['0'],
            'characterspell_set-0-points': ['0'],
            'characterspell_set-0-skill': [str(skill.id)],
            'characterspell_set-0-spell': [str(spell.id)],
        }

        # Create new CharacterSpell object.
        response = self.client.post(self.path, data)
        self.assertRedirects(
            response,
            reverse(
                'gurps-manager-character-id-spells',
                args=[self.character.id]
            )
        )

    def test_post_failure_v1(self):
        """Update a character's spells, but with invalid data."""
        data = {
            'characterspell_set-INITIAL_FORMS': ['0'],
            'characterspell_set-TOTAL_FORMS': ['1'],
            'characterspell_set-MAX_NUM_FORMS': ['10'],
        }
        response = self.client.post(self.path, data)
        self.assertRedirects(
            response,
            reverse(
                'gurps-manager-character-id-spells-update-form',
                args=[self.character.id]
            )
        )

    def test_post_failure_v2(self):
        """Update a character's spells, but without the rights to do so."""
        character = factories.CharacterFactory.create()
        path = reverse('gurps-manager-character-id-spells', args=[character.id])
        response = self.client.post(path, {})
        self.assertEqual(response.status_code, 403)

    def test_get(self):
        """GET ``self.path``."""
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)

    def test_get_bad_id(self):
        """GET ``self.path`` with a bad ID."""
        self.character.delete()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 404)

    def test_get_failure(self):
        """Let some other user own ``self.character``, then GET ``self.path``.""" # pylint: disable=C0301
        self.character.owner = factories.UserFactory.create()
        self.character.save()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 403)

    def test_put(self):
        """POST ``self.path`` and emulate a PUT request."""
        response = self.client.put(self.path, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """POST ``self.path`` and emulate a DELETE request."""
        response = self.client.delete(self.path, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

class CharacterIdPossessionsUpdateFormTestCase(TestCase):
    """Tests for the ``character/<id>/possessions/update-form/`` path."""
    def setUp(self):
        """Create a character and set ``self.path``.

        The created character is accessible as ``self.character``.

        """
        user = _login(self.client)[0]
        self.character = factories.CharacterFactory.create(owner=user)
        self.path = reverse(
            'gurps-manager-character-id-possessions-update-form',
            args=[self.character.id]
        )

    def test_login_required(self):
        """Ensure user must be logged in to GET this URL."""
        _test_login_required(self, self.path)

    def test_post(self):
        """POST ``self.path``."""
        response = self.client.post(self.path)
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.path``."""
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)

    def test_get_bad_id(self):
        """GET ``self.path`` with a bad ID."""
        self.character.delete()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 404)

    def test_get_failure(self):
        """Let some other user own ``self.character``, then GET ``self.path``.""" # pylint: disable=C0301
        self.character.owner = factories.UserFactory.create()
        self.character.save()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 403)

    def test_put(self):
        """POST ``self.path`` and emulate a PUT request."""
        response = self.client.put(self.path, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """POST ``self.path`` and emulate a DELETE request."""
        response = self.client.delete(self.path, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

class CharacterIdPossessionsTestCase(TestCase):
    """Tests for the ``character/<id>/possessions/`` path."""
    def setUp(self):
        """Create a character and set ``self.path``.

        The created character is accessible as ``self.character``.

        """
        user = _login(self.client)[0]
        self.character = factories.CharacterFactory.create(owner=user)
        self.path = reverse(
            'gurps-manager-character-id-possessions',
            args=[self.character.id]
        )

    def test_login_required(self):
        """Ensure user must be logged in to GET this URL."""
        _test_login_required(self, self.path)

    def test_post(self):
        """Update a character's possessions."""
        self.character.campaign.skillsets.add(
            models.SkillSet.objects.get(name__exact='Professional')
        )
        item = factories.ItemFactory.create(campaign=self.character.campaign)
        data = {
            'possession_set-INITIAL_FORMS': ['0'],
            'possession_set-TOTAL_FORMS': ['1'],
            'possession_set-MAX_NUM_FORMS': ['10'],

            'possession_set-0-id': [''],
            'possession_set-0-character': [str(self.character.id)],
            'possession_set-0-quantity': ['1'],
            'possession_set-0-skill': [str(
                # This skill belongs to the 'Professional' skillset.
                models.Skill.objects.get(name__exact='Abacus').id
            )],
            'possession_set-0-item': [str(item.id)],
        }

        response = self.client.post(self.path, data)
        self.assertRedirects(
            response,
            reverse(
                'gurps-manager-character-id-possessions',
                args=[self.character.id]
            )
        )

    def test_post_failure_v1(self):
        """Update a character's possessions, but with invalid data."""
        self.character.campaign.skillsets.clear()
        data = {
            'possession_set-INITIAL_FORMS': ['0'],
            'possession_set-TOTAL_FORMS': ['1'],
            'possession_set-MAX_NUM_FORMS': ['10'],
            'possession_set-0-quantity': ['-1'],
        }
        response = self.client.post(self.path, data)
        self.assertRedirects(
            response,
            reverse(
                'gurps-manager-character-id-possessions-update-form',
                args=[self.character.id]
            )
        )

    def test_post_failure_v2(self):
        """Update a character's possessions, but without the rights to do so."""
        character = factories.CharacterFactory.create()
        path = reverse(
            'gurps-manager-character-id-possessions',
            args=[character.id]
        )
        response = self.client.post(path, {})
        self.assertEqual(response.status_code, 403)

    def test_get(self):
        """GET ``self.path``."""
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)

    def test_get_bad_id(self):
        """GET ``self.path`` with a bad ID."""
        self.character.delete()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 404)

    def test_get_failure(self):
        """Let some other user own ``self.character``, then GET ``self.path``.""" # pylint: disable=C0301
        self.character.owner = factories.UserFactory.create()
        self.character.save()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 403)

    def test_put(self):
        """POST ``self.path`` and emulate a PUT request."""
        response = self.client.put(self.path, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """POST ``self.path`` and emulate a DELETE request."""
        response = self.client.delete(self.path, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

class CharacterIdTraitsUpdateFormTestCase(TestCase):
    """Tests for the ``character/<id>/traits/update-form/`` path."""
    def setUp(self):
        """Create a character and set ``self.path``.

        The created character is accessible as ``self.character``.

        """
        user = _login(self.client)[0]
        self.character = factories.CharacterFactory.create(owner=user)
        self.path = reverse(
            'gurps-manager-character-id-traits-update-form',
            args=[self.character.id]
        )

    def test_login_required(self):
        """Ensure user must be logged in to GET this URL."""
        _test_login_required(self, self.path)

    def test_post(self):
        """POST ``self.path``."""
        response = self.client.post(self.path)
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.path``."""
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)

    def test_get_bad_id(self):
        """GET ``self.path`` with a bad ID."""
        self.character.delete()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 404)

    def test_get_failure(self):
        """Let some other user own ``self.character``, then GET ``self.path``.""" # pylint: disable=C0301
        self.character.owner = factories.UserFactory.create()
        self.character.save()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 403)

    def test_put(self):
        """POST ``self.path`` and emulate a PUT request."""
        response = self.client.put(self.path, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """POST ``self.path`` and emulate a DELETE request."""
        response = self.client.delete(self.path, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

class CharacterIdTraitsTestCase(TestCase):
    """Tests for the ``character/<id>/traits/`` path."""
    def setUp(self):
        """Create a character and set ``self.path``.

        The created character is accessible as ``self.character``.

        """
        user = _login(self.client)[0]
        self.character = factories.CharacterFactory.create(owner=user)
        self.path = reverse(
            'gurps-manager-character-id-traits',
            args=[self.character.id]
        )

    def test_login_required(self):
        """Ensure user must be logged in to GET this URL."""
        _test_login_required(self, self.path)

    def test_post(self):
        """Create a trait for a character."""
        data = {
            'trait_set-INITIAL_FORMS': ['0'],
            'trait_set-TOTAL_FORMS': ['1'],
            'trait_set-MAX_NUM_FORMS': ['10'],
            'trait_set-0-character': [str(self.character.id)],
            'trait_set-0-id': [''], # no id, b/c creating new trait
            'trait_set-0-name': ['bombastic'],
            'trait_set-0-description': [''],
            'trait_set-0-points': ['1'],
        }
        response = self.client.post(self.path, data)
        self.assertRedirects(
            response,
            reverse(
                'gurps-manager-character-id-traits',
                args=[self.character.id]
            )
        )

    def test_post_failure_v1(self):
        """Create a trait, but for a non-existent character."""
        self.character.delete()
        response = self.client.post(self.path, {})
        self.assertEqual(response.status_code, 404)

    def test_post_failure_v2(self):
        """Create a trait for a character, but with invalid data."""
        data = {
            'trait_set-INITIAL_FORMS': ['0'],
            'trait_set-TOTAL_FORMS': ['1'],
            'trait_set-MAX_NUM_FORMS': ['10'],
            'trait_set-0-points': ['-1'],
        }
        response = self.client.post(self.path, data)
        self.assertRedirects(
            response,
            reverse(
                'gurps-manager-character-id-traits-update-form',
                args=[self.character.id]
            )
        )

    def test_post_failure_v3(self):
        """Create a trait for a character, but without rights to do so."""
        path = reverse(
            'gurps-manager-character-id-traits',
            args=[factories.CharacterFactory.create().id]
        )
        data = {
            'trait_set-INITIAL_FORMS': ['0'],
            'trait_set-TOTAL_FORMS': ['1'],
            'trait_set-MAX_NUM_FORMS': ['10'],
        }
        response = self.client.post(path, data)
        self.assertEqual(response.status_code, 403)

    def test_get(self):
        """GET ``self.path``."""
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)

    def test_get_bad_id(self):
        """GET ``self.path`` with a bad ID."""
        self.character.delete()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 404)

    def test_get_failure(self):
        """Let some other user own ``self.character``, then GET ``self.path``.""" # pylint: disable=C0301
        self.character.owner = factories.UserFactory.create()
        self.character.save()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 403)

    def test_put(self):
        """POST ``self.path`` and emulate a PUT request."""
        response = self.client.put(self.path, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """POST ``self.path`` and emulate a DELETE request."""
        response = self.client.delete(self.path, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

class CharacterIdHitLocationsUpdateFormTestCase(TestCase):
    """Tests for the ``character/<id>/hit-locations/update-form/`` path."""
    def setUp(self):
        """Create a character and set ``self.path``.

        The created character is accessible as ``self.character``.

        """
        user = _login(self.client)[0]
        self.character = factories.CharacterFactory.create(owner=user)
        self.path = reverse(
            'gurps-manager-character-id-hit-locations-update-form',
            args=[self.character.id]
        )

    def test_login_required(self):
        """Ensure user must be logged in to GET this URL."""
        _test_login_required(self, self.path)

    def test_post(self):
        """POST ``self.path``."""
        response = self.client.post(self.path)
        self.assertEqual(response.status_code, 405)

    def test_get(self):
        """GET ``self.path``."""
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)

    def test_get_bad_id(self):
        """GET ``self.path`` with a bad ID."""
        self.character.delete()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 404)

    def test_get_failure(self):
        """Let some other user own ``self.character``, then GET ``self.path``.""" # pylint: disable=C0301
        self.character.owner = factories.UserFactory.create()
        self.character.save()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 403)

    def test_put(self):
        """POST ``self.path`` and emulate a PUT request."""
        response = self.client.put(self.path, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """POST ``self.path`` and emulate a DELETE request."""
        response = self.client.delete(self.path, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

class CharacterIdHitLocationsTestCase(TestCase):
    """Tests for the ``character/<id>/hit-locations/`` path."""
    def setUp(self):
        """Create a character and set ``self.path``.

        The created character is accessible as ``self.character``.

        """
        user = _login(self.client)[0]
        self.character = factories.CharacterFactory.create(owner=user)
        self.path = reverse(
            'gurps-manager-character-id-hit-locations',
            args=[self.character.id]
        )

    def test_login_required(self):
        """Ensure user must be logged in to GET this URL."""
        _test_login_required(self, self.path)

    def test_post(self):
        """Create a hit location on a character."""
        data = {
            'hitlocation_set-INITIAL_FORMS': ['0'],
            'hitlocation_set-TOTAL_FORMS': ['1'],
            'hitlocation_set-MAX_NUM_FORMS': ['10'],
            'hitlocation_set-0-id': [''],
            'hitlocation_set-0-character': [str(self.character.id)],
            'hitlocation_set-0-damage_resistance': ['3'],
            'hitlocation_set-0-damage_taken': ['0'],
            'hitlocation_set-0-name': ['head'],
            'hitlocation_set-0-passive_damage_resistance': ['2'],
            'hitlocation_set-0-status': [''],
        }
        response = self.client.post(self.path, data)
        self.assertRedirects(
            response,
            reverse(
                'gurps-manager-character-id-hit-locations',
                args=[self.character.id]
            )
        )

    def test_post_failure_v1(self):
        """Create a hit location, but for a non-existent character."""
        self.character.delete()
        response = self.client.post(self.path, {})
        self.assertEqual(response.status_code, 404)

    def test_post_failure_v2(self):
        """Create a hit location, but with invalid data."""
        data = {
            'hitlocation_set-INITIAL_FORMS': ['0'],
            'hitlocation_set-TOTAL_FORMS': ['1'],
            'hitlocation_set-MAX_NUM_FORMS': ['10'],
            'hitlocation_set-0-damage_taken': ['-1'],
        }
        response = self.client.post(self.path, data)
        self.assertRedirects(
            response,
            reverse(
                'gurps-manager-character-id-hit-locations-update-form',
                args=[self.character.id]
            )
        )

    def test_post_failure_v3(self):
        """Create a hit location, but without rights to do so."""
        path = reverse(
            'gurps-manager-character-id-hit-locations',
            args=[factories.CharacterFactory.create().id]
        )
        data = {
            'trait_set-INITIAL_FORMS': ['0'],
            'trait_set-TOTAL_FORMS': ['1'],
            'trait_set-MAX_NUM_FORMS': ['10'],
        }
        response = self.client.post(path, data)
        self.assertEqual(response.status_code, 403)

    def test_get(self):
        """GET ``self.path``."""
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)

    def test_get_bad_id(self):
        """GET ``self.path`` with a bad ID."""
        self.character.delete()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 404)

    def test_get_failure(self):
        """Let some other user own ``self.character``, then GET ``self.path``.""" # pylint: disable=C0301
        self.character.owner = factories.UserFactory.create()
        self.character.save()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 403)

    def test_put(self):
        """POST ``self.path`` and emulate a PUT request."""
        response = self.client.put(self.path, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        """POST ``self.path`` and emulate a DELETE request."""
        response = self.client.delete(self.path, {'_method': 'DELETE'})
        self.assertEqual(response.status_code, 405)

def _login(client):
    """Create a user and log it in to ``client``.

    Return the User object and its plaintext password as a two-element list.

    """
    user, password = factories.create_user()
    client.login(username=user.username, password=password)
    return [user, password]

def _test_login_required(test_case, url=None):
    """Logout ``test_case.client``, then GET ``url``.

    ``test_case`` is an instance of a ``TestCase`` subclass. A caller should
    typically pass ``self`` to this method.

    ``url`` is a string such as ``campaign/15/``. If no value is provided,
    ``url`` defaults to ``test_case.URL``.

    This method logs out the test client, then attempts to GET ``url``. The
    client should be redirected to the ``gurps-manager-login`` view with the
    ``next`` URL argument set to ``url``.

    """
    if url is None:
        url = test_case.PATH
    test_case.client.logout()
    test_case.assertRedirects(
        test_case.client.get(url),
        '{}?next={}'.format(reverse('gurps-manager-login'), url)
    )
