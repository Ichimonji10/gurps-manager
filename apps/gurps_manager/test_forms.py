"""Unit tests for the ``forms`` module.

Each test case in this module tests a single form. For example, the
``CampaignFormTestCase`` tests just the ``CampaignForm`` form.

"""
from django.test import TestCase
from gurps_manager import factories, forms

# pylint: disable=E1101
# Class 'FooForm' has no 'create' member (no-member)
# Instance of 'FooForm' has no 'is_valid' member (no-member)
# Instance of 'FooFormTestCase' has no 'assertTrue' member (no-member)
#
# pylint: disable=R0904
# Classes inheriting from TestCase will have 60+ too many public methods, and
# that's not something I have control over. Ignore it.

class CampaignFormTestCase(TestCase):
    """Tests for ``CampaignForm``."""
    def test_valid(self):
        """Create a valid CampaignForm."""
        form = forms.CampaignForm({'name': factories.campaign_name()})
        self.assertTrue(form.is_valid())

    def test_missing_name(self):
        """Create a CampaignForm without setting ``name``."""
        form = forms.CampaignForm({})
        self.assertFalse(form.is_valid())

    def test_has_description(self):
        """Create a CampaignForm and set ``description``."""
        form = forms.CampaignForm({
            'name': factories.campaign_name(),
            'description': factories.campaign_description(),
        })
        self.assertTrue(form.is_valid())
