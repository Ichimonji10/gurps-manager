"""Unit tests for the ``tables`` module.

Each test case in this module tests a single table. For example, the
``CampaignTableTestCase`` tests just the ``CampaignTable`` table.

"""
from django.test import TestCase
from gurps_manager import factories, models, tables

# pylint: disable=E1101
# Class 'FooForm' has no 'create' member (no-member)
# Instance of 'FooForm' has no 'is_valid' member (no-member)
# Instance of 'FooFormTestCase' has no 'assertTrue' member (no-member)
#
# pylint: disable=R0904
# Classes inheriting from TestCase will have 60+ too many public methods, and
# that's not something I have control over. Ignore it.

class CampaignTableTestCase(TestCase):
    """Tests for ``CampaignTable``."""
    def setUp(self):
        """Instantiate a ``CampaignTable`` object."""
        self.user = factories.UserFactory.create()
        table_cls = tables.campaign_table(self.user)
        self.table = table_cls(models.Campaign.objects.all())

    def test_render_description(self):
        """Test method ``render_description``."""
        string = factories._random_str(130, 150)
        self.assertEqual(
            self.table.render_description(string),
            tables._truncate_string(string) # pylint: disable=W0212
        )

    def test_render_actions_v1(self):
        """Test method ``render_actions``."""
        campaign = factories.CampaignFactory.create()
        self.assertTrue(issubclass(
            type(self.table.render_actions(campaign)),
            str
        ))

    def test_render_actions_v2(self):
        """Test method ``render_actions``."""
        campaign = factories.CampaignFactory.create(owner=self.user)
        self.assertTrue(issubclass(
            type(self.table.render_actions(campaign)),
            str
        ))

class CharacterTableTestCase(TestCase):
    """Tests for ``CharacterTable``."""
    def setUp(self):
        """Instantiate a ``CharacterTable`` object."""
        self.user = factories.UserFactory.create()
        table_cls = tables.character_table(self.user)
        self.table = table_cls(models.Character.objects.all())

    def test_render_spent_points(self):
        """Test method ``render_spent_points``."""
        character = factories.CharacterFactory.create()
        self.assertEqual(
            self.table.render_spent_points(character),
            character.total_points_spent()
        )

    def test_render_description(self):
        """Test method ``render_description``."""
        string = factories._random_str(130, 150)
        self.assertEqual(
            self.table.render_description(string),
            tables._truncate_string(string) # pylint: disable=W0212
        )

    def test_render_actions_v1(self):
        """Test method ``render_actions``."""
        character = factories.CharacterFactory.create()
        self.assertTrue(issubclass(
            type(self.table.render_actions(character)),
            str
        ))

    def test_render_actions_v2(self):
        """Test method ``render_actions``."""
        character = factories.CharacterFactory.create(owner=self.user)
        self.assertTrue(issubclass(
            type(self.table.render_actions(character)),
            str
        ))
