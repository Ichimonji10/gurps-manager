"""Unit tests for the ``views`` module.

Each test case  in this module tests a single view. For example,
``CampaignCreateFormTestCase`` tests just the ``campaign_create_form`` view.

"""
from django.core.urlresolvers import reverse
from django.test import TestCase
from gurps_manager import factories, models
import unittest

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
        """POST ``self.PATH``, thus logging in."""
        user, password = factories.create_user()
        response = self.client.post(
            self.PATH,
            {'username': user.username, 'password': password}
        )
        self.assertRedirects(response, reverse('gurps-manager-index'))

    def test_post_failure(self):
        """POST ``self.PATH``, incorrectly."""
        response = self.client.post(self.PATH, {})
        self.assertRedirects(response, self.PATH)

    def test_get(self):
        """GET ``self.PATH``."""
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

    def test_put(self):
        """POST ``self.path`` and emulate a PUT request."""
        data = factories.CampaignFactory.attributes()
        data['owner'].save()
        data['owner'] = self.campaign.owner.id
        data['_method'] = 'PUT'
        response = self.client.post(self.path, data)
        self.assertRedirects(response, self.path)

    def test_put_failure(self):
        """POST ``self.path`` and emulate a PUT request, incorrectly."""
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

    def test_delete(self):
        """POST ``self.path`` and emulate a DELETE request."""
        response = self.client.post(self.path, {'_method': 'DELETE'})
        self.assertRedirects(response, reverse('gurps-manager-campaign'))

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
        """GET ``self.path``."""
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)

    def test_get_bad_id(self):
        """GET ``self.path`` with a bad ID."""
        self.campaign.delete()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 404)

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
        """GET ``self.path``."""
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)

    def test_get_bad_id(self):
        """GET ``self.path`` with a bad ID."""
        self.campaign.delete()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 404)

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

    @unittest.skip('Have not figured out how to correctly construct this test.')
    def test_post(self):
        """POST ``self.path``."""
        # TODO: Find out how to make this test work
        pass

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

    @unittest.skip('Have not figured out how to correctly construct this test.')
    def test_post(self):
        """POST ``self.path``."""
        # TODO: Find out how to make this test work
        pass

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

    @unittest.skip('Have not figured out how to correctly construct this test.')
    def test_post(self):
        """POST ``self.path``."""
        # TODO: Find out how to make this test work
        pass

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

    @unittest.skip('Have not figured out how to correctly construct this test.')
    def test_post(self):
        """POST ``self.path``."""
        # TODO: Find out how to make this test work
        pass

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

    @unittest.skip('Have not figured out how to correctly construct this test.')
    def test_post(self):
        """POST ``self.path``."""
        # TODO: Find out how to make this test work
        pass

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

    @unittest.skip('Have not figured out how to correctly construct this test.')
    def test_post(self):
        """POST ``self.path``."""
        # TODO: Find out how to make this test work
        pass

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

    @unittest.skip('Have not figured out how to correctly construct this test.')
    def test_post(self):
        """POST ``self.path``."""
        # TODO: Find out how to make this test work
        pass

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
