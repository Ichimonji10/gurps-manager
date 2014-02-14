"""Unit tests for the ``models`` module.

Each test case in this module tests a single model. For example, the
``CampaignTestCase`` tests just the ``Campaign`` model.

"""
from django.test import TestCase
from gurps_manager import factories

# pylint: disable=E1101
# E: 16,19: Class 'CampaignFactory' has no 'build' member (no-member)
# Pylint does not detect the build and create methods provided by factory_boy.
#
# pylint: disable=R0904
# R: 11, 0: Too many public methods (72/20) (too-many-public-methods)
# All classes inheriting from TestCase will cause this warning.

class CampaignTestCase(TestCase):
    """Tests for ``Campaign``."""
    def test_str(self):
        """Test the ``__str__`` method."""
        name = factories.campaign_name()
        campaign = factories.CampaignFactory.build(name=name)
        self.assertEqual(name, str(campaign))

class CharacterTestCase(TestCase):
    """Tests for ``Character``."""
    def test_str(self):
        """Test the ``__str__`` method."""
        name = factories.character_name()
        character = factories.CharacterFactory.build(name=name)
        self.assertEqual(name, str(character))

    def test_fatigue(self):
        """Test the ``fatigue`` method."""
        strength = factories.character_intfield()
        bonus_fatigue = factories.character_intfield()
        character = factories.CharacterFactory.build(
            strength=strength,
            bonus_fatigue=bonus_fatigue,
        )
        self.assertEqual(character.fatigue(), strength + bonus_fatigue)

    def test_hitpoints(self):
        """Test the ``hitpoints`` method."""
        health = factories.character_intfield()
        bonus_hitpoints = factories.character_intfield()
        character = factories.CharacterFactory.build(
            health=health,
            bonus_hitpoints=bonus_hitpoints,
        )
        self.assertEqual(character.hitpoints(), health + bonus_hitpoints)

    def test_alertness(self):
        """Test the ``alertness`` method."""
        intelligence = factories.character_intfield()
        bonus_alertness = factories.character_intfield()
        character = factories.CharacterFactory.build(
            intelligence=intelligence,
            bonus_alertness=bonus_alertness,
        )
        self.assertEqual(character.alertness(), intelligence + bonus_alertness)

    def test_will(self):
        """Test the ``will`` method."""
        intelligence = factories.character_intfield()
        bonus_willpower = factories.character_intfield()
        character = factories.CharacterFactory.build(
            intelligence=intelligence,
            bonus_willpower=bonus_willpower,
        )
        self.assertEqual(character.will(), intelligence + bonus_willpower)

    def test_fright(self):
        """Test the ``fright`` method."""
        intelligence = factories.character_intfield()
        bonus_fright = factories.character_intfield()
        character = factories.CharacterFactory.build(
            intelligence=intelligence,
            bonus_fright=bonus_fright,
        )
        self.assertEqual(character.fright(), intelligence + bonus_fright)

    def test_initiative(self):
        """Test the ``initiative`` method."""
        bonus_initiative = factories.character_intfield()
        dexterity = factories.character_intfield()
        intelligence = factories.character_intfield()
        character = factories.CharacterFactory.build(
            bonus_initiative=bonus_initiative,
            dexterity=dexterity,
            intelligence=intelligence,
        )
        self.assertEqual(
            character.initiative(),
            ((intelligence + dexterity) / 4) + bonus_initiative,
        )

    def test_no_encumbrance(self):
        """Test the ``no_encumbrance`` method."""
        strength = factories.character_intfield()
        character = factories.CharacterFactory.build(strength=strength)
        self.assertEqual(character.no_encumbrance(), strength * 2)

    def test_light_encumbrance(self):
        """Test the ``light_encumbrance`` method."""
        strength = factories.character_intfield()
        character = factories.CharacterFactory.build(strength=strength)
        self.assertEqual(character.light_encumbrance(), strength * 4)

    def test_medium_encumbrance(self):
        """Test the ``medium_encumbrance`` method."""
        strength = factories.character_intfield()
        character = factories.CharacterFactory.build(strength=strength)
        self.assertEqual(character.medium_encumbrance(), strength * 6)

    def test_heavy_encumbrance(self):
        """Test the ``heavy_encumbrance`` method."""
        strength = factories.character_intfield()
        character = factories.CharacterFactory.build(strength=strength)
        self.assertEqual(character.heavy_encumbrance(), strength * 12)

    def test_extra_heavy_encumbrance(self):
        """Test the ``extra_heavy_encumbrance`` method."""
        strength = factories.character_intfield()
        character = factories.CharacterFactory.build(strength=strength)
        self.assertEqual(character.extra_heavy_encumbrance(), strength * 20)

    def test_total_possession_weight(self):
        """Test the ``total_possession_weight`` method."""
        # Zero items.
        character = factories.CharacterFactory.create()
        self.assertEqual(0, character.total_possession_weight())

        # One item.
        possession1 = factories.PossessionFactory.create(character=character)
        total_weight = possession1.item.weight * possession1.quantity
        self.assertEqual(total_weight, character.total_possession_weight())

        # Two items.
        possession2 = factories.PossessionFactory.create(character=character)
        total_weight += possession2.item.weight * possession2.quantity
        self.assertEqual(total_weight, character.total_possession_weight())

    def test_total_possession_value(self):
        """Test the ``total_possession_value`` method."""
        # Zero items.
        character = factories.CharacterFactory.create()
        self.assertEqual(0, character.total_possession_value())

        # One item.
        possession1 = factories.PossessionFactory.create(character=character)
        total_value = possession1.item.value * possession1.quantity
        self.assertEqual(total_value, character.total_possession_value())

        # Two items.
        possession2 = factories.PossessionFactory.create(character=character)
        total_value += possession2.item.value * possession2.quantity
        self.assertEqual(total_value, character.total_possession_value())

    def test_encumbrance_penalty(self):
        """Test the ``encumbrance_penalty`` method."""
        character = factories.CharacterFactory.create()

        # total_possession_weight < no_encumbrance
        character.total_possession_weight = lambda: 0
        character.no_encumbrance = lambda: 1
        self.assertEqual(character.encumbrance_penalty(), 0)

        # total_possession_weight < light_encumbrance
        character.total_possession_weight = lambda: 1
        character.light_encumbrance = lambda: 2
        self.assertEqual(character.encumbrance_penalty(), 1)

        # total_possession_weight < medium_encumbrance
        character.total_possession_weight = lambda: 2
        character.medium_encumbrance = lambda: 3
        self.assertEqual(character.encumbrance_penalty(), 2)

        # total_possession_weight < heavy_encumbrance
        character.total_possession_weight = lambda: 3
        character.heavy_encumbrance = lambda: 4
        self.assertEqual(character.encumbrance_penalty(), 3)

        # total_possession_weight < extra_heavy_encumbrance
        character.total_possession_weight = lambda: 4
        character.extra_heavy_encumbrance = lambda: 5
        self.assertEqual(character.encumbrance_penalty(), 4)

        # total_possession_weight >= extra_heavy_encumbrance
        character.total_possession_weight = lambda: 5
        self.assertTrue(character.encumbrance_penalty() >= 5)

class SkillSetTestCase(TestCase):
    """Tests for ``SkillSet``."""
    def test_str(self):
        """Test the ``__str__`` method."""
        name = factories.skillset_name()
        skillset = factories.SkillSetFactory.build(name=name)
        self.assertEqual(name, str(skillset))

class SkillTestCase(TestCase):
    """Tests for ``Skill``."""
    def test_str(self):
        """Test the ``__str__`` method."""
        name = factories.skill_name()
        skill = factories.SkillFactory.build(name=name)
        self.assertEqual(name, str(skill))

class TraitTestCase(TestCase):
    """Tests for ``Trait``."""
    def test_str(self):
        """Test the ``__str__`` method."""
        name = factories.trait_name()
        trait = factories.TraitFactory.build(name=name)
        self.assertEqual(name, str(trait))

class ItemTestCase(TestCase):
    """Tests for ``Item``."""
    def test_str(self):
        """Test the ``__str__`` method."""
        name = factories.item_name()
        item = factories.ItemFactory.build(name=name)
        self.assertEqual(name, str(item))

class SpellTestCase(TestCase):
    """Tests for ``Spell``."""
    def test_str(self):
        """Test the ``__str__`` method."""
        name = factories.spell_name()
        spell = factories.SpellFactory.build(name=name)
        self.assertEqual(name, str(spell))

class HitLocationTestCase(TestCase):
    """Tests for ``HitLocation``."""
    def test_str(self):
        """Test the ``__str__`` method."""
        name = factories.hitlocation_name()
        hitlocation = factories.HitLocationFactory.build(name=name)
        self.assertEqual(name, str(hitlocation))
