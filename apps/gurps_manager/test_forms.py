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

class CharacterFormTestCase(TestCase):
    """Tests for ``CharacterForm``."""
    @classmethod
    def _character_attributes(cls):
        """Return a dict of attributes for populating a CharacterForm."""
        return {
            'campaign': factories.CampaignFactory.create().id,

            # many-to-fields
            # 'skills', 'spells', and 'items' are optional

            # string-based fields
            # 'description' and 'story' are optional
            'name': factories.character_name(),

            # integer fields
            'strength': factories.character_intfield(),
            'dexterity': factories.character_intfield(),
            'intelligence': factories.character_intfield(),
            'health': factories.character_intfield(),
            'magery': factories.character_intfield(),
            'bonus_fatigue': factories.character_intfield(),
            'bonus_hitpoints': factories.character_intfield(),
            'bonus_alertness': factories.character_intfield(),
            'bonus_willpower': factories.character_intfield(),
            'bonus_fright': factories.character_intfield(),
            'bonus_speed': factories.character_intfield(),
            'bonus_movement': factories.character_intfield(),
            'bonus_dodge': factories.character_intfield(),
            'bonus_initiative': factories.character_intfield(),
            'free_strength': factories.character_intfield(),
            'free_dexterity': factories.character_intfield(),
            'free_intelligence': factories.character_intfield(),
            'free_health': factories.character_intfield(),

            # float fields
            'total_points': factories.character_floatfield(),
            'used_fatigue': factories.character_floatfield(),

            # lookup fields
            'appearance': factories.character_lookupfield(),
            'wealth': factories.character_lookupfield(),
            'eidetic_memory': factories.character_lookupfield(),
            'muscle_memory': factories.character_lookupfield(),
        }

    def test_valid(self):
        """Create a valid CharacterForm."""
        form = forms.CharacterForm(self._character_attributes())
        self.assertTrue(form.is_valid())

    def test_has_description(self):
        """Create a CharacterForm and set ``description``."""
        attributes = self._character_attributes()
        attributes['description'] = factories.character_description()
        form = forms.CharacterForm(attributes)
        self.assertTrue(form.is_valid())

    def test_has_story(self):
        """Create a CharacterForm and set ``story``."""
        attributes = self._character_attributes()
        attributes['story'] = factories.character_story()
        form = forms.CharacterForm(attributes)
        self.assertTrue(form.is_valid())

    def test_missing_everything(self):
        """Create a CharacterForm and set no fields."""
        form = forms.CharacterForm({})
        self.assertFalse(form.is_valid())

    def test_missing_campaign(self):
        """Create a CharacterForm without setting ``campaign``."""
        attributes = self._character_attributes()
        del attributes['campaign']
        form = forms.CharacterForm(attributes)
        self.assertFalse(form.is_valid())

    def test_missing_name(self):
        """Create a CharacterForm without setting ``name``."""
        attributes = self._character_attributes()
        del attributes['name']
        form = forms.CharacterForm(attributes)
        self.assertFalse(form.is_valid())

    def test_missing_strength(self):
        """Create a CharacterForm without setting ``strength``."""
        attributes = self._character_attributes()
        del attributes['strength']
        form = forms.CharacterForm(attributes)
        self.assertFalse(form.is_valid())

    def test_missing_dexterity(self):
        """Create a CharacterForm without setting ``dexterity``."""
        attributes = self._character_attributes()
        del attributes['dexterity']
        form = forms.CharacterForm(attributes)
        self.assertFalse(form.is_valid())

    def test_missing_intelligence(self):
        """Create a CharacterForm without setting ``intelligence``."""
        attributes = self._character_attributes()
        del attributes['intelligence']
        form = forms.CharacterForm(attributes)
        self.assertFalse(form.is_valid())

    def test_missing_health(self):
        """Create a CharacterForm without setting ``health``."""
        attributes = self._character_attributes()
        del attributes['health']
        form = forms.CharacterForm(attributes)
        self.assertFalse(form.is_valid())

    def test_missing_appearance(self):
        """Create a CharacterForm without setting ``appearance``."""
        attributes = self._character_attributes()
        del attributes['appearance']
        form = forms.CharacterForm(attributes)
        self.assertFalse(form.is_valid())

    def test_missing_wealth(self):
        """Create a CharacterForm without setting ``wealth``."""
        attributes = self._character_attributes()
        del attributes['wealth']
        form = forms.CharacterForm(attributes)
        self.assertFalse(form.is_valid())

    def test_missing_magery(self):
        """Create a CharacterForm without setting ``magery``."""
        attributes = self._character_attributes()
        del attributes['magery']
        form = forms.CharacterForm(attributes)
        self.assertFalse(form.is_valid())

    def test_missing_eidetic_memory(self):
        """Create a CharacterForm without setting ``eidetic_memory``."""
        attributes = self._character_attributes()
        del attributes['eidetic_memory']
        form = forms.CharacterForm(attributes)
        self.assertFalse(form.is_valid())

    def test_missing_muscle_memory(self):
        """Create a CharacterForm without setting ``muscle_memory``."""
        attributes = self._character_attributes()
        del attributes['muscle_memory']
        form = forms.CharacterForm(attributes)
        self.assertFalse(form.is_valid())

    def test_missing_bonus_fatigue(self):
        """Create a CharacterForm without setting ``bonus_fatigue``."""
        attributes = self._character_attributes()
        del attributes['bonus_fatigue']
        form = forms.CharacterForm(attributes)
        self.assertFalse(form.is_valid())

    def test_missing_bonus_hitpoints(self):
        """Create a CharacterForm without setting ``bonus_hitpoints``."""
        attributes = self._character_attributes()
        del attributes['bonus_hitpoints']
        form = forms.CharacterForm(attributes)
        self.assertFalse(form.is_valid())

    def test_missing_bonus_alertness(self):
        """Create a CharacterForm without setting ``bonus_alertness``."""
        attributes = self._character_attributes()
        del attributes['bonus_alertness']
        form = forms.CharacterForm(attributes)
        self.assertFalse(form.is_valid())

    def test_missing_bonus_willpower(self):
        """Create a CharacterForm without setting ``bonus_willpower``."""
        attributes = self._character_attributes()
        del attributes['bonus_willpower']
        form = forms.CharacterForm(attributes)
        self.assertFalse(form.is_valid())

    def test_missing_bonus_fright(self):
        """Create a CharacterForm without setting ``bonus_fright``."""
        attributes = self._character_attributes()
        del attributes['bonus_fright']
        form = forms.CharacterForm(attributes)
        self.assertFalse(form.is_valid())

    def test_missing_bonus_speed(self):
        """Create a CharacterForm without setting ``bonus_speed``."""
        attributes = self._character_attributes()
        del attributes['bonus_speed']
        form = forms.CharacterForm(attributes)
        self.assertFalse(form.is_valid())

    def test_missing_bonus_movement(self):
        """Create a CharacterForm without setting ``bonus_movement``."""
        attributes = self._character_attributes()
        del attributes['bonus_movement']
        form = forms.CharacterForm(attributes)
        self.assertFalse(form.is_valid())

    def test_missing_bonus_dodge(self):
        """Create a CharacterForm without setting ``bonus_dodge``."""
        attributes = self._character_attributes()
        del attributes['bonus_dodge']
        form = forms.CharacterForm(attributes)
        self.assertFalse(form.is_valid())

    def test_missing_bonus_initiative(self):
        """Create a CharacterForm without setting ``bonus_initiative``."""
        attributes = self._character_attributes()
        del attributes['bonus_initiative']
        form = forms.CharacterForm(attributes)
        self.assertFalse(form.is_valid())

    def test_missing_free_strength(self):
        """Create a CharacterForm without setting ``free_strength``."""
        attributes = self._character_attributes()
        del attributes['free_strength']
        form = forms.CharacterForm(attributes)
        self.assertFalse(form.is_valid())

    def test_missing_free_dexterity(self):
        """Create a CharacterForm without setting ``free_dexterity``."""
        attributes = self._character_attributes()
        del attributes['free_dexterity']
        form = forms.CharacterForm(attributes)
        self.assertFalse(form.is_valid())

    def test_missing_free_intelligence(self):
        """Create a CharacterForm without setting ``free_intelligence``."""
        attributes = self._character_attributes()
        del attributes['free_intelligence']
        form = forms.CharacterForm(attributes)
        self.assertFalse(form.is_valid())

    def test_missing_free_health(self):
        """Create a CharacterForm without setting ``free_health``."""
        attributes = self._character_attributes()
        del attributes['free_health']
        form = forms.CharacterForm(attributes)
        self.assertFalse(form.is_valid())

    def test_missing_total_points(self):
        """Create a CharacterForm without setting ``total_points``."""
        attributes = self._character_attributes()
        del attributes['total_points']
        form = forms.CharacterForm(attributes)
        self.assertFalse(form.is_valid())

    def test_missing_used_fatigue(self):
        """Create a CharacterForm without setting ``used_fatigue``."""
        attributes = self._character_attributes()
        del attributes['used_fatigue']
        form = forms.CharacterForm(attributes)
        self.assertFalse(form.is_valid())
