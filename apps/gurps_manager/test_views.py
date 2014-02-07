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

class CampaignTestCase(TestCase):
    """Tests for the ``campaign/`` path."""
    PATH = reverse('gurps-manager-campaign')

    def test_post(self):
        """POST ``self.PATH``."""
        num_campaigns = models.Campaign.objects.count()
        response = self.client.post(
            self.PATH,
            factories.CampaignFactory.attributes()
        )
        self.assertEqual(models.Campaign.objects.count(), num_campaigns + 1)
        self.assertRedirects(
            response,
            reverse(
                'gurps-manager-campaign-id',
                args=[models.Campaign.objects.latest('id').id]
            )
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
        response = self.client.delete(self.PATH, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

class CampaignCreateFormTestCase(TestCase):
    """Tests for the ``campaign/create-form/`` path."""
    PATH = reverse('gurps-manager-campaign-create-form')

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
        response = self.client.delete(self.PATH, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

class CampaignIdTestCase(TestCase):
    """Tests for the ``campaign/<id>/`` path."""
    def setUp(self):
        """Create a campaign and set ``self.path``.

        The created campaign is accessible as ``self.campaign``.

        """
        self.campaign = factories.CampaignFactory.create()
        self.path = reverse(
            'gurps-manager-campaign-id',
            args=[self.campaign.id]
        )

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
        data['_method'] = 'PUT'
        response = self.client.post(self.path, data)
        self.assertRedirects(response, self.path)

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
        self.campaign = factories.CampaignFactory.create()
        self.path = reverse(
            'gurps-manager-campaign-id-update-form',
            args=[self.campaign.id]
        )

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
        response = self.client.delete(self.path, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)

class CampaignIdDeleteFormTestCase(TestCase):
    """Tests for the ``campaign/<id>/delete-form/`` path."""
    def setUp(self):
        """Create a campaign and set ``self.path``.

        The created campaign is accessible as ``self.campaign``.

        """
        self.campaign = factories.CampaignFactory.create()
        self.path = reverse(
            'gurps-manager-campaign-id-delete-form',
            args=[self.campaign.id]
        )

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
        response = self.client.delete(self.path, {'_method': 'PUT'})
        self.assertEqual(response.status_code, 405)
