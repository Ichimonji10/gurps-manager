"""Unit tests for the ``views`` module.

Each test case  in this module tests a single view. For example,
``CampaignCreateFormTestCase`` tests just the ``campaign_create_form`` view.

"""
from django.core.urlresolvers import reverse
from django.test import TestCase
from gurps_manager import factories, models

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
                args = [models.Campaign.objects.latest('id').id]
            )
        )

    def test_get(self):
        """GET ``self.PATH``."""
        response = self.client.get(self.PATH)
        self.assertEqual(response.status_code, 200)

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

class CampaignIdTestCase(TestCase):
    """Tests for the ``campaign/<id>/`` path."""
    def setUp(self):
        """Create a campaign and set ``self.path``.

        The created campaign is accessible as ``self.campaign``.

        """
        self.campaign = factories.CampaignFactory.create()
        self.path = reverse(
            'gurps-manager-campaign-id',
            args = [self.campaign.id]
        )

    def test_get(self):
        """GET ``self.path``."""
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)

    def test_get_bad_id(self):
        """GET ``self.path`` with a bad ID."""
        self.campaign.delete()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 404)
