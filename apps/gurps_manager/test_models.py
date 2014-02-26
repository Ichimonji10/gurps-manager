"""Unit tests for the ``models`` module.

Each test case in this module tests a single model. For example, the
``CampaignTestCase`` tests just the ``Campaign`` model.

"""
from django.test import TestCase
from gurps_manager import factories, models
from math import floor
import random

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
        self.assertEqual(
            character.encumbrance_penalty(),
            floor(character.speed()) + character.bonus_movement + 1
        )

    def test_speed(self):
        """Test the ``speed`` method."""
        char = factories.CharacterFactory.create()

        # Character does not have the "running" skill.
        speed = ((char.dexterity + char.health) / 4) + char.bonus_speed
        self.assertEqual(char.speed(), speed)

        # Create a "running" skill. Link it to the test character.
        char_skill = factories.CharacterSkillFactory(
            character=char,
            skill=factories.SkillFactory(name='RuNnInG')
        )
        self.assertEqual(char.speed(), speed + (char_skill.score() / 8))

    def test_movement(self):
        """Test the ``movement`` method."""
        character = factories.CharacterFactory.create()
        character_movement = floor(character.speed()) \
            - character.encumbrance_penalty() \
            + character.bonus_movement
        self.assertEqual(character.movement(), character_movement)

    def test_dodge(self):
        """Test the ``dodge`` method."""
        character = factories.CharacterFactory.create()
        character_dodge = floor(character.speed()) \
            - character.encumbrance_penalty() \
            + character.bonus_dodge
        self.assertEqual(character.dodge(), character_dodge)

    def test_points_in_strength(self):
        """Test the ``points_in_strength`` method."""
        character = factories.CharacterFactory.create()
        self.assertEqual(
            character.points_in_strength(),
            character._points_in_attribute( # pylint: disable=W0212
                character.strength - character.free_strength
            )
        )

    def test_points_in_dexterity(self):
        """Test the ``points_in_dexterity`` method."""
        character = factories.CharacterFactory.create()
        self.assertEqual(
            character.points_in_dexterity(),
            character._points_in_attribute( # pylint: disable=W0212
                character.dexterity - character.free_dexterity
            )
        )

    def test_points_in_intelligence(self):
        """Test the ``points_in_intelligence`` method."""
        character = factories.CharacterFactory.create()
        self.assertEqual(
            character.points_in_intelligence(),
            character._points_in_attribute( # pylint: disable=W0212
                character.intelligence - character.free_intelligence
            )
        )

    def test_points_in_health(self):
        """Test the ``points_in_health`` method."""
        character = factories.CharacterFactory.create()
        self.assertEqual(
            character.points_in_health(),
            character._points_in_attribute( # pylint: disable=W0212
                character.health - character.free_health
            )
        )

    def test_points_in_attribute(self):
        """Test the ``_points_in_attribute`` method."""
        character = factories.CharacterFactory.create()

        # 8 > level
        level = random.randrange(-1000, 8)
        self.assertEqual(
            character._points_in_attribute(level), # pylint: disable=W0212
            (9 - level) * -10
        )

        # 9 > level
        self.assertEqual(character._points_in_attribute(8), -15) # pylint: disable=W0212

        # 14 > level
        level = random.randrange(9, 14)
        self.assertEqual(
            character._points_in_attribute(level), # pylint: disable=W0212
            (level - 10) * 10
        )

        # 15 > level
        self.assertEqual(character._points_in_attribute(14), 45) # pylint: disable=W0212

        # 18 > level
        level = random.randrange(15, 18)
        self.assertEqual(
            character._points_in_attribute(level), # pylint: disable=W0212
            (level - 12) * 20
        )

        # 18 <= level
        level = random.randrange(18, 1000)
        self.assertEqual(
            character._points_in_attribute(level), # pylint: disable=W0212
            (level - 13) * 25
        )

    def test_points_in_magery_v1(self):
        """Test the ``points_in_magery`` method."""
        character = factories.CharacterFactory.create(magery=0)
        self.assertEqual(character.points_in_magery(), 0)

    def test_points_in_magery_v2(self):
        """Test the ``points_in_magery`` method. Use a non-zero magery."""
        magery = factories.character_intfield()
        if magery == 0:
            magery += 1
        character = factories.CharacterFactory.create(magery=magery)
        self.assertEqual(
            character.points_in_magery(),
            (character.magery * 10) + 5
        )

    def test_total_points_in_attributes(self):
        """Test the ``total_points_in_attributes`` method."""
        character = factories.CharacterFactory.create()
        self.assertEqual(
            character.total_points_in_attributes(),
            character.points_in_strength() \
                + character.points_in_dexterity() \
                + character.points_in_intelligence() \
                + character.points_in_health()
        )

    def test_total_points_in_skills(self):
        """Test the ``total_points_in_skills`` method."""
        # Zero skills.
        character = factories.CharacterFactory.create()
        self.assertEqual(0, character.total_points_in_skills())

        # One skill.
        skill1 = factories.CharacterSkillFactory.create(character=character)
        self.assertEqual(skill1.points, character.total_points_in_skills())

        # Two skills.
        skill2 = factories.CharacterSkillFactory.create(character=character)
        self.assertEqual(
            skill1.points + skill2.points,
            character.total_points_in_skills()
        )

    def test_total_points_in_spells(self):
        """Test the ``total_points_in_spells`` method."""
        # Zero spells.
        character = factories.CharacterFactory.create()
        self.assertEqual(0, character.total_points_in_spells())

        # One spell.
        spell1 = factories.CharacterSpellFactory.create(character=character)
        self.assertEqual(spell1.points, character.total_points_in_spells())

        # Two spells.
        spell2 = factories.CharacterSpellFactory.create(character=character)
        self.assertEqual(
            spell1.points + spell2.points,
            character.total_points_in_spells()
        )

    def test_total_points_in_advantages(self):
        """Test the ``total_points_in_advantages`` method."""
        character = factories.CharacterFactory.create()

        # Zero traits.
        points = 0
        self.assertEqual(points, character.total_points_in_advantages())

        # One trait.
        trait1 = factories.TraitFactory.create(character=character)
        if trait1.points > 0:
            points += trait1.points
        self.assertEqual(points, character.total_points_in_advantages())

        # Two traits.
        trait2 = factories.TraitFactory.create(character=character)
        if trait2.points > 0:
            points += trait2.points
        self.assertEqual(points, character.total_points_in_advantages())

    def test_total_points_in_disadvantages(self): # pylint: disable=C0103
        """Test the ``total_points_in_disadvantages`` method."""
        character = factories.CharacterFactory.create()

        # Zero traits.
        points = 0
        self.assertEqual(points, character.total_points_in_disadvantages())

        # One trait.
        trait1 = factories.TraitFactory.create(character=character)
        if trait1.points < 0:
            points += trait1.points
        self.assertEqual(points, character.total_points_in_disadvantages())

        # Two traits.
        trait2 = factories.TraitFactory.create(character=character)
        if trait2.points < 0:
            points += trait2.points
        self.assertEqual(points, character.total_points_in_disadvantages())

    def test_total_points_in_special_traits(self): # pylint: disable=C0103
        """Test the ``total_points_in_special_traits`` method."""
        character = factories.CharacterFactory.create()
        self.assertEqual(
            character.total_points_in_special_traits(),
            character.eidetic_memory \
                + character.muscle_memory \
                + character.wealth \
                + character.appearance \
                + character.points_in_magery()
        )

    def test_total_points_spent(self):
        """Test the ``total_points_spent`` method."""
        character = factories.CharacterFactory.create()
        self.assertEqual(
            character.total_points_spent(),
            character.total_points_in_attributes() \
                + character.total_points_in_advantages() \
                + character.total_points_in_disadvantages() \
                + character.total_points_in_skills() \
                + character.total_points_in_spells() \
                + character.total_points_in_special_traits()
        )

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

class CharacterSkillTestCase(TestCase):
    """Tests for ``CharacterSkill``."""
    def test_score_v1(self):
        """Create a 'Mental' skill, then test method ``score``."""
        skill = factories.SkillFactory(
            category=models.Skill.get_category_id('Mental')
        )
        character_skill = factories.CharacterSkillFactory.create(skill=skill)
        self.assertEqual(
            character_skill.score(),
            character_skill._mental_skill_score( # pylint: disable=W0212
                character_skill.character.intelligence
            )
        )

    def test_score_v2(self):
        """Create a 'Mental (health)' skill, then test method ``score``."""
        skill = factories.SkillFactory(
            category=models.Skill.get_category_id('Mental (health)')
        )
        character_skill = factories.CharacterSkillFactory.create(skill=skill)
        self.assertEqual(
            character_skill.score(),
            character_skill._mental_skill_score( # pylint: disable=W0212
                character_skill.character.health
            )
        )

    def test_score_v3(self):
        """Create a 'Physical' skill, then test method ``score``."""
        skill = factories.SkillFactory(
            category=models.Skill.get_category_id('Physical')
        )
        character_skill = factories.CharacterSkillFactory.create(skill=skill)
        self.assertEqual(
            character_skill.score(),
            character_skill._physical_skill_score( # pylint: disable=W0212
                character_skill.character.dexterity
            )
        )

    def test_score_v4(self):
        """Create a 'Physical (health)' skill, then test method ``score``."""
        skill = factories.SkillFactory(
            category=models.Skill.get_category_id('Physical (health)')
        )
        character_skill = factories.CharacterSkillFactory.create(skill=skill)
        self.assertEqual(
            character_skill.score(),
            character_skill._physical_skill_score( # pylint: disable=W0212
                character_skill.character.health
            )
        )

    def test_score_v5(self):
        """Create a 'Physical (strength)' skill, then test method ``score``."""
        skill = factories.SkillFactory(
            category=models.Skill.get_category_id('Physical (strength)')
        )
        character_skill = factories.CharacterSkillFactory.create(skill=skill)
        self.assertEqual(
            character_skill.score(),
            character_skill._physical_skill_score( # pylint: disable=W0212
                character_skill.character.strength
            )
        )

    def test_score_v6(self):
        """Create a 'Psionic' skill, then test method ``score``."""
        skill = factories.SkillFactory(
            category=models.Skill.get_category_id('Psionic')
        )
        character_skill = factories.CharacterSkillFactory.create(skill=skill)
        self.assertEqual(
            character_skill.score(),
            character_skill._psionic_skill_score() # pylint: disable=W0212
        )

    def test_score_v7(self):
        """Create an invalid skill, then test method ``score``."""
        skill = factories.SkillFactory(category=7)
        character_skill = factories.CharacterSkillFactory.create(skill=skill)
        self.assertRaises(ValueError, character_skill.score)

    def test_mental_skill_score_v1(self):
        """Test method ``_mental_skill_score``."""
        character_skill = factories.CharacterSkillFactory.create()
        character_skill._effective_points_mental = lambda: 0.25
        attribute = random.randrange(-100, 100)
        self.assertEqual(character_skill._mental_skill_score(attribute), 0)

    def test_mental_skill_score_v2(self):
        """Test method ``_mental_skill_score``."""
        character_skill = factories.CharacterSkillFactory.create()
        character_skill._effective_points_mental = lambda: 0.75
        attribute = random.randrange(-100, 100)
        self.assertEqual(
            character_skill._mental_skill_score(attribute),
            attribute - character_skill.skill.difficulty
        )

    def test_mental_skill_score_v3(self):
        """Test method ``_mental_skill_score``."""
        character_skill = factories.CharacterSkillFactory.create()
        character_skill._effective_points_mental = lambda: 1.5
        attribute = random.randrange(-100, 100)
        self.assertEqual(
            character_skill._mental_skill_score(attribute),
            attribute - character_skill.skill.difficulty + 1
        )

    def test_mental_skill_score_v4(self):
        """Test method ``_mental_skill_score``."""
        character_skill = factories.CharacterSkillFactory.create()
        character_skill._effective_points_mental = lambda: 3
        attribute = random.randrange(-100, 100)
        self.assertEqual(
            character_skill._mental_skill_score(attribute),
            attribute - character_skill.skill.difficulty + 2
        )

    def test_mental_skill_score_v5(self):
        """Test method ``_mental_skill_score``."""
        character_skill = factories.CharacterSkillFactory.create(
            skill=factories.SkillFactory.create(difficulty=3)
        )
        character_skill._effective_points_mental = lambda: 4
        attribute = random.randrange(-100, 100)
        self.assertEqual(
            character_skill._mental_skill_score(attribute),
            attribute \
                - character_skill.skill.difficulty \
                + (character_skill._effective_points_mental() // 2) \
                + 1
        )

    def test_mental_skill_score_v6(self):
        """Test method ``_mental_skill_score``."""
        character_skill = factories.CharacterSkillFactory.create(
            skill=factories.SkillFactory.create(difficulty=4)
        )
        character_skill._effective_points_mental = lambda: 4
        attribute = random.randrange(-100, 100)
        self.assertEqual(
            character_skill._mental_skill_score(attribute),
            attribute \
                - character_skill.skill.difficulty \
                + (character_skill._effective_points_mental() // 4) \
                + 2
        )

    def test_psionic_skill_score_v1(self):
        """Test method ``_psionic_skill_score``."""
        character_skill = factories.CharacterSkillFactory.create(points=0.25)
        self.assertEqual(character_skill._psionic_skill_score(), 0) # pylint: disable=W0212

    def test_psionic_skill_score_v2(self):
        """Test method ``_psionic_skill_score``."""
        character_skill = factories.CharacterSkillFactory.create(points=0.75)
        self.assertEqual(
            character_skill._psionic_skill_score(), # pylint: disable=W0212
            character_skill.character.intelligence \
                - character_skill.skill.difficulty
        )

    def test_psionic_skill_score_v3(self):
        """Test method ``_psionic_skill_score``."""
        character_skill = factories.CharacterSkillFactory.create(points=1.5)
        self.assertEqual(
            character_skill._psionic_skill_score(), # pylint: disable=W0212
            character_skill.character.intelligence \
                - character_skill.skill.difficulty \
                + 1
        )

    def test_psionic_skill_score_v4(self):
        """Test method ``_psionic_skill_score``."""
        character_skill = factories.CharacterSkillFactory.create(points=3)
        self.assertEqual(
            character_skill._psionic_skill_score(), # pylint: disable=W0212
            character_skill.character.intelligence \
                - character_skill.skill.difficulty \
                + 2
        )

    def test_psionic_skill_score_v5(self):
        """Test method ``_psionic_skill_score``."""
        character_skill = factories.CharacterSkillFactory.create(
            points=3,
            skill=factories.SkillFactory(difficulty=3)
        )
        self.assertEqual(
            character_skill._psionic_skill_score(), # pylint: disable=W0212
            character_skill.character.intelligence \
                - character_skill.skill.difficulty \
                + (character_skill.points // 2) \
                + 1
        )

    def test_psionic_skill_score_v6(self):
        """Test method ``_psionic_skill_score``."""
        character_skill = factories.CharacterSkillFactory.create(
            points=4,
            skill=factories.SkillFactory(difficulty=4)
        )
        self.assertEqual(
            character_skill._psionic_skill_score(), # pylint: disable=W0212
            character_skill.character.intelligence \
                - character_skill.skill.difficulty \
                + (character_skill.points // 4) \
                + 2
        )

class CharacterSpellTestCase(TestCase):
    """Tests for ``CharacterSpell``."""
    def test_score_v1(self):
        """Test method ``score``.

        Use a ``CharacterSpell`` having 0.0 points.

        """
        char_spell = factories.CharacterSpellFactory(points=0)
        self.assertEqual(char_spell.score(), 0)

    def test_score_v2(self):
        """Test method ``score``.

        Use a ``CharacterSpell`` having 0.75 points.

        """
        char_spell = factories.CharacterSpellFactory(points=0.75)
        self.assertEqual(char_spell.score(), char_spell._base_score()) # pylint: disable=W0212

    def test_score_v3(self):
        """Test method ``score``.

        Use a ``CharacterSpell`` having 1.5 points.

        """
        char_spell = factories.CharacterSpellFactory(points=1.5)
        self.assertEqual(char_spell.score(), char_spell._base_score() + 1) # pylint: disable=W0212

    def test_score_v4(self):
        """Test method ``score``.

        Use a ``CharacterSpell`` having 3.0 points.

        """
        char_spell = factories.CharacterSpellFactory(points=3)
        self.assertEqual(char_spell.score(), char_spell._base_score() + 2) # pylint: disable=W0212

    def test_score_v5(self):
        """Test method ``score``.

        Use a ``CharacterSpell`` having 5.0 points and a 'Hard' ``Spell``.

        """
        # FIXME: Properly reference the spell's difficulty. No magic numbers.
        spell = factories.SpellFactory(difficulty=3)
        char_spell = factories.CharacterSpellFactory(points=5, spell=spell)
        self.assertEqual(
            char_spell.score(),
            char_spell._base_score() + (char_spell.points // 2) + 1 # pylint: disable=W0212
        )

    def test_score_v6(self):
        """Test method ``score``.

        Use a ``CharacterSpell`` having 5.0 points and a 'Very Hard' ``Spell``.

        """
        # FIXME: Properly reference the spell's difficulty. No magic numbers.
        spell = factories.SpellFactory(difficulty=4)
        char_spell = factories.CharacterSpellFactory(points=5, spell=spell)
        self.assertEqual(
            char_spell.score(),
            char_spell._base_score() + (char_spell.points // 4) + 2 # pylint: disable=W0212
        )
