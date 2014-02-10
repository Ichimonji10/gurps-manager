"""Factory Boy factory definitions.

These factory definitions are used as an alternative to plain old Django
fixtures. Rather than simply defining a static set of test data, factories can
be used to generate disgustingly random data. (perfect for testing!)

"""
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyAttribute
from factory import SubFactory
from gurps_manager import models
import random

class CampaignFactory(DjangoModelFactory):
    """Instantiate a ``gurps_manager.models.Campaign`` object.

    >>> CampaignFactory.build().full_clean()
    >>> CampaignFactory.create().id is None
    False

    """
    # pylint: disable=R0903
    # pylint: disable=W0232
    FACTORY_FOR = models.Campaign
    name = FuzzyAttribute(lambda: campaign_name()) # pylint: disable=W0108

def campaign_name():
    """Return a value for the ``Campaign.name`` model attribute.

    >>> from gurps_manager.models import Campaign
    >>> name = campaign_name()
    >>> isinstance(name, str)
    True
    >>> len(name) >= 1
    True
    >>> len(name) <= Campaign.MAX_LEN_NAME
    True

    """
    return _random_str(1, models.Campaign.MAX_LEN_NAME)

def campaign_description():
    """Return a value for the ``Campaign.description`` model attribute.

    >>> from gurps_manager.models import Campaign
    >>> description = campaign_description()
    >>> isinstance(description, str)
    True
    >>> len(description) >= 1
    True
    >>> len(description) <= Campaign.MAX_LEN_DESCRIPTION
    True

    """
    return _random_str(1, models.Campaign.MAX_LEN_DESCRIPTION)

class CharacterFactory(DjangoModelFactory):
    """Instantiate a ``gurps_manager.models.Character`` object.

    >>> character = CharacterFactory.create()
    >>> character.full_clean()
    >>> character.id is None
    False

    """
    # pylint: disable=R0903
    # pylint: disable=W0232
    # pylint: disable=W0108
    FACTORY_FOR = models.Character

    campaign = SubFactory(CampaignFactory)
    name = FuzzyAttribute(lambda: character_name())

    # integer-based fields
    strength = FuzzyAttribute(lambda: character_intfield())
    dexterity = FuzzyAttribute(lambda: character_intfield())
    intelligence = FuzzyAttribute(lambda: character_intfield())
    health = FuzzyAttribute(lambda: character_intfield())
    magery = FuzzyAttribute(lambda: character_intfield())
    bonus_fatigue = FuzzyAttribute(lambda: character_intfield())
    bonus_hitpoints = FuzzyAttribute(lambda: character_intfield())
    bonus_alertness = FuzzyAttribute(lambda: character_intfield())
    bonus_willpower = FuzzyAttribute(lambda: character_intfield())
    bonus_fright = FuzzyAttribute(lambda: character_intfield())
    bonus_speed = FuzzyAttribute(lambda: character_intfield())
    bonus_movement = FuzzyAttribute(lambda: character_intfield())
    bonus_dodge = FuzzyAttribute(lambda: character_intfield())
    bonus_initiative = FuzzyAttribute(lambda: character_intfield())
    free_strength = FuzzyAttribute(lambda: character_intfield())
    free_dexterity = FuzzyAttribute(lambda: character_intfield())
    free_intelligence = FuzzyAttribute(lambda: character_intfield())
    free_health = FuzzyAttribute(lambda: character_intfield())

    # float-based fields
    total_points = FuzzyAttribute(lambda: character_floatfield())
    used_fatigue = FuzzyAttribute(lambda: character_floatfield())

    # lookup fields
    appearance = FuzzyAttribute(lambda: character_appearance())
    wealth = FuzzyAttribute(lambda: character_wealth())
    eidetic_memory = FuzzyAttribute(lambda: character_eidetic_memory())
    muscle_memory = FuzzyAttribute(lambda: character_muscle_memory())

def character_name():
    """Return a value for the ``Character.name`` model attribute.

    >>> from gurps_manager.models import Character
    >>> name = character_name()
    >>> isinstance(name, str)
    True
    >>> len(name) >= 1
    True
    >>> len(name) <= Character.MAX_LEN_NAME
    True

    """
    return _random_str(1, models.Character.MAX_LEN_NAME)

def character_description():
    """Return a value for the ``Character.description`` model attribute.

    >>> from gurps_manager.models import Character
    >>> description = character_description()
    >>> isinstance(description, str)
    True
    >>> len(description) >= 1
    True
    >>> len(description) <= Character.MAX_LEN_DESCRIPTION
    True

    """
    return _random_str(1, models.Character.MAX_LEN_DESCRIPTION)

def character_story():
    """Return a value for the ``Character.story`` model attribute.

    >>> from gurps_manager.models import Character
    >>> story = character_story()
    >>> isinstance(story, str)
    True
    >>> len(story) >= 1
    True
    >>> len(story) <= Character.MAX_LEN_STORY
    True

    """
    return _random_str(1, models.Character.MAX_LEN_STORY)

def character_intfield():
    """Return a value for an int-based ``Character`` model attribute.

    >>> isinstance(character_intfield(), int)
    True

    """
    # FIXME: what are valud values for this field?
    return random.randint(0, 100)

def character_floatfield():
    """Return a value for an float-based ``Character`` model attribute.

    >>> from gurps_manager.models import validate_quarter
    >>> value = character_floatfield()
    >>> isinstance(value, float)
    True
    >>> validate_quarter(value)

    """
    # FIXME: what are valid values for this field?
    return 0.25 * random.randint(0, 400)

def character_appearance():
    """Return a value for the ``Character.appearance`` model attribute.

    >>> isinstance(character_appearance(), int)
    True

    """
    return random.choice([-30, -25, -20, -10, -5, 0, 5, 15, 25, 35])

def character_wealth():
    """Return a value for the ``Character.wealth`` model attribute.

    >>> isinstance(character_wealth(), int)
    True

    """
    return random.choice([-25, -15, -10, 0, 10, 20, 30, 50])

def character_eidetic_memory():
    """Return a value for the ``Character.eidetic_memory`` model attribute.

    >>> isinstance(character_eidetic_memory(), int)
    True

    """
    return random.choice([0, 30, 60])

def character_muscle_memory():
    """Return a value for the ``Character.muscle_memory`` model attribute.

    >>> isinstance(character_muscle_memory(), int)
    True

    """
    return random.choice([0, 30, 60])

class SkillSetFactory(DjangoModelFactory):
    """Instantiate a ``gurps_manager.models.SkillSet`` object.

    >>> SkillSetFactory.build().full_clean()
    >>> SkillSetFactory.create().id is None
    False

    """
    # pylint: disable=R0903
    # pylint: disable=W0232
    FACTORY_FOR = models.SkillSet
    name = FuzzyAttribute(lambda: skillset_name()) # pylint: disable=W0108

def skillset_name():
    """Return a value for the ``SkillSet.name`` model attribute.

    >>> from gurps_manager.models import SkillSet
    >>> name = skillset_name()
    >>> isinstance(name, str)
    True
    >>> len(name) >= 1
    True
    >>> len(name) <= SkillSet.MAX_LEN_NAME
    True

    """
    return _random_str(1, models.SkillSet.MAX_LEN_NAME)

class SkillFactory(DjangoModelFactory):
    """Instantiate a ``gurps_manager.models.Skill`` object.

    >>> skill = SkillFactory.create()
    >>> skill.full_clean()
    >>> skill.id is None
    False

    """
    # pylint: disable=R0903
    # pylint: disable=W0232
    FACTORY_FOR = models.Skill
    name = FuzzyAttribute(lambda: skill_name()) # pylint: disable=W0108
    category = FuzzyAttribute(lambda: skill_category()) # pylint: disable=W0108
    difficulty = FuzzyAttribute(lambda: skill_difficulty()) # pylint: disable=W0108
    skillset = SubFactory(SkillSetFactory)

def skill_name():
    """Return a value for the ``Skill.name`` model attribute.

    >>> from gurps_manager.models import Skill
    >>> name = skill_name()
    >>> isinstance(name, str)
    True
    >>> len(name) >= 1
    True
    >>> len(name) <= Skill.MAX_LEN_NAME
    True

    """
    return _random_str(1, models.Skill.MAX_LEN_NAME)

def skill_category():
    """Return a value for the ``Skill.category`` model attribute.

    >>> from gurps_manager.models import Skill
    >>> category = skill_category()
    >>> isinstance(category, int)
    True
    >>> category in [choice[0] for choice in Skill.CATEGORY_CHOICES]
    True

    """
    # `choice` returns tuple like (1, 'Mental'). Return the integer part.
    return random.choice(models.Skill.CATEGORY_CHOICES)[0]

def skill_difficulty():
    """Return a value for the ``Skill.difficulty`` model attribute.

    >>> from gurps_manager.models import Skill
    >>> difficulty = skill_difficulty()
    >>> isinstance(difficulty, int)
    True
    >>> difficulty in [choice[0] for choice in Skill.DIFFICULTY_CHOICES]
    True

    """
    # `choice` returns a tuple like (1, 'Easy'). Return the integer part.
    return random.choice(models.Skill.DIFFICULTY_CHOICES)[0]

class CharacterSkillFactory(DjangoModelFactory):
    """Instantiate a ``gurps_manager.models.CharacterSkill`` object.

    >>> characterskill = CharacterSkillFactory.create()
    >>> characterskill.full_clean()
    >>> characterskill.id is None
    False

    """
    # pylint: disable=R0903
    # pylint: disable=W0232
    FACTORY_FOR = models.CharacterSkill
    skill = SubFactory(SkillFactory)
    character = SubFactory(CharacterFactory)
    bonus_level = FuzzyAttribute(lambda: characterskill_bonus_level()) # pylint: disable=W0108
    points = FuzzyAttribute(lambda: characterskill_points()) # pylint: disable=W0108

def characterskill_bonus_level():
    """Return a value for the ``CharacterSkill.bonus_level`` model attribute.

    >>> isinstance(characterskill_bonus_level(), int)
    True

    """
    # FIXME: what are valid values for this field?
    return random.randrange(-100, 100)

def characterskill_points():
    """Return a value for the ``CharacterSkill.points`` model attribute.

    >>> from gurps_manager.models import validate_quarter
    >>> points = characterskill_points()
    >>> isinstance(points, float)
    True
    >>> validate_quarter(points)

    """
    # FIXME: what are valid values for this field?
    return 0.25 * random.randint(0, 400)

class TraitFactory(DjangoModelFactory):
    """Instantiate a ``gurps_manager.models.Trait`` object.

    >>> trait = TraitFactory.create()
    >>> trait.full_clean()
    >>> trait.id is None
    False

    """
    # pylint: disable=R0903
    # pylint: disable=W0232
    FACTORY_FOR = models.Trait
    name = FuzzyAttribute(lambda: trait_name()) # pylint: disable=W0108
    points = FuzzyAttribute(lambda: trait_points()) # pylint: disable=W0108
    character = SubFactory(CharacterFactory)

def trait_name():
    """Return a value for the ``Trait.name`` model attribute.

    >>> from gurps_manager.models import Trait
    >>> name = trait_name()
    >>> isinstance(name, str)
    True
    >>> len(name) >= 1
    True
    >>> len(name) <= Trait.MAX_LEN_NAME
    True

    """
    return _random_str(1, models.Trait.MAX_LEN_NAME)

def trait_points():
    """Return a value for the ``Trait.points`` model attribute.

    >>> from gurps_manager.models import validate_quarter
    >>> points = trait_points()
    >>> isinstance(points, float)
    True
    >>> validate_quarter(points)

    """
    # FIXME: what are valid values for this field?
    return 0.25 * random.randint(0, 400)

class ItemFactory(DjangoModelFactory):
    """Instantiate a ``gurps_manager.models.Item`` object.

    >>> ItemFactory.build().full_clean()
    >>> ItemFactory.create().id is None
    False

    """
    # pylint: disable=R0903
    # pylint: disable=W0232
    FACTORY_FOR = models.Item
    name = FuzzyAttribute(lambda: item_name()) # pylint: disable=W0108
    cost = FuzzyAttribute(lambda: item_cost()) # pylint: disable=W0108
    weight = FuzzyAttribute(lambda: item_weight()) # pylint: disable=W0108

def item_name():
    """Return a value for the ``Item.name`` model attribute.

    >>> from gurps_manager.models import Item
    >>> name = item_name()
    >>> isinstance(name, str)
    True
    >>> len(name) >= 1
    True
    >>> len(name) <= Item.MAX_LEN_NAME
    True

    """
    return _random_str(1, models.Item.MAX_LEN_NAME)

def item_cost():
    """Return a value for the ``Item.cost`` model attribute.

    >>> from gurps_manager.models import validate_not_negative
    >>> cost = item_cost()
    >>> isinstance(cost, float)
    True
    >>> validate_not_negative(cost)

    """
    # FIXME: what are valid values for this field?
    return random.random() * 100

def item_weight():
    """Return a value for the ``Item.weight`` model attribute.

    >>> from gurps_manager.models import validate_not_negative
    >>> weight = item_weight()
    >>> isinstance(weight, float)
    True
    >>> validate_not_negative(weight)

    """
    # FIXME: what are valid values for this field?
    return random.random() * 100

class PossessionFactory(DjangoModelFactory):
    """Instantiate a ``gurps_manager.models.Possession`` object.

    >>> possession = PossessionFactory.create()
    >>> possession.full_clean()
    >>> possession.id is None
    False

    """
    # pylint: disable=R0903
    # pylint: disable=W0232
    FACTORY_FOR = models.Possession
    character = SubFactory(CharacterFactory)
    item = SubFactory(ItemFactory)
    quantity = FuzzyAttribute(lambda: possession_quantity()) # pylint: disable=W0108

def possession_quantity():
    """Return a value for the ``Possession.quantity`` model attribute.

    >>> from gurps_manager.models import validate_not_negative
    >>> quantity = possession_quantity()
    >>> isinstance(quantity, int)
    True
    >>> validate_not_negative(quantity)

    """
    # FIXME: what are valid values for this field?
    return random.randrange(0, 100)

class SpellFactory(DjangoModelFactory):
    """Instantiate a ``gurps_manager.models.Spell`` object.

    >>> SpellFactory.build().full_clean()
    >>> SpellFactory.create().id is None
    False

    """
    # pylint: disable=R0903
    # pylint: disable=W0232
    FACTORY_FOR = models.Spell
    name = FuzzyAttribute(lambda: spell_name()) # pylint: disable=W0108
    school = FuzzyAttribute(lambda: spell_school()) # pylint: disable=W0108
    resist = FuzzyAttribute(lambda: spell_resist()) # pylint: disable=W0108
    duration = FuzzyAttribute(lambda: spell_duration()) # pylint: disable=W0108
    cast_time = FuzzyAttribute(lambda: spell_cast_time()) # pylint: disable=W0108
    difficulty = FuzzyAttribute(lambda: spell_difficulty()) # pylint: disable=W0108
    initial_fatigue_cost = FuzzyAttribute(lambda: spell_initial_fatigue_cost()) # pylint: disable=W0108
    maintenance_fatigue_cost = FuzzyAttribute(lambda: spell_maintenance_fatigue_cost()) # pylint: disable=W0108

def spell_name():
    """Return a value for the ``Spell.name`` model attribute.

    >>> from gurps_manager.models import Spell
    >>> name = spell_name()
    >>> isinstance(name, str)
    True
    >>> len(name) >= 1
    True
    >>> len(name) <= Spell.MAX_LEN_NAME
    True

    """
    return _random_str(1, models.Spell.MAX_LEN_NAME)

def spell_school():
    """Return a value for the ``Spell.school`` model attribute.

    >>> from gurps_manager.models import Spell
    >>> school = spell_school()
    >>> isinstance(school, str)
    True
    >>> len(school) >= 1
    True
    >>> len(school) <= Spell.MAX_LEN_SCHOOL
    True

    """
    return _random_str(1, models.Spell.MAX_LEN_SCHOOL)

def spell_resist():
    """Return a value for the ``Spell.resist`` model attribute.

    >>> from gurps_manager.models import Spell
    >>> resist = spell_resist()
    >>> isinstance(resist, str)
    True
    >>> len(resist) >= 1
    True
    >>> len(resist) <= Spell.MAX_LEN_RESIST
    True

    """
    return _random_str(1, models.Spell.MAX_LEN_RESIST)

def spell_duration():
    """Return a value for the ``Spell.duration`` model attribute.

    >>> isinstance(spell_duration(), int)
    True

    """
    # FIXME: what are valid values for this field?
    return random.randrange(-100, 100)

def spell_cast_time():
    """Return a value for the ``Spell.cast_time`` model attribute.

    >>> isinstance(spell_duration(), int)
    True

    """
    # FIXME: what are valid values for this field?
    return random.randrange(-100, 100)

def spell_difficulty():
    """Return a value for the ``Spell.difficulty`` model attribute.

    >>> from gurps_manager.models import Spell
    >>> difficulty = spell_difficulty()
    >>> isinstance(difficulty, int)
    True
    >>> difficulty in [choice[0] for choice in Spell.DIFFICULTY_CHOICES]
    True

    """
    # `choice` returns tuple like (3, 'Hard'). Return the integer part.
    return random.choice(models.Spell.DIFFICULTY_CHOICES)[0]

def spell_initial_fatigue_cost():
    """Return a value for the ``Spell.initial_fatigue_cost`` model attribute.

    >>> isinstance(spell_duration(), int)
    True

    """
    # FIXME: what are valid values for this field?
    return random.randrange(-100, 100)

def spell_maintenance_fatigue_cost():
    """Return a value for the ``Spell.maintenance_fatigue_cost`` attribute.

    >>> isinstance(spell_duration(), int)
    True

    """
    # FIXME: what are valid values for this field?
    return random.randrange(-100, 100)

#-------------------------------------------------------------------------------

def _random_int(lower, upper):
    """Return a random integer between ``lower`` and ``upper``, inclusive.

    If ``lower >= upper``, return ``lower``.

    >>> _random_int(0, 0)
    0
    >>> _random_int(5, 5)
    5
    >>> _random_int(5, 0)
    5
    >>> _random_int(0, 5) in range(0, 6)
    True

    """
    if lower >= upper:
        return lower
    return random.randint(0, upper - lower) + lower

def _random_str(min_len=0, max_len=0):
    """Return a string consisting of random UTF-8 characters.

    If ``min_len >= max_len``, return a string exactly ``min_len`` characters
    long. Otherwise, return a string between ``min_len`` and ``max_len`` chars
    long, inclusive.

    From RFC 3629:

        The definition of UTF-8 prohibits encoding character numbers between
        U+D800 and U+DFFF, which are reserved for use with the UTF-16 encoding
        form (as surrogate pairs) and do not directly represent characters.

    Thus, bytes 0 through 0xD7FF are used to generate random characters. It is
    possible to use an even greater range of values, but this range should be
    enough for any sane use of this application. See also:
    http://docs.python.org/3/library/functions.html#chr

    """
    string = ''
    for i in range(_random_int(min_len, max_len)):
        string += chr(random.randrange(0, 0xD7FF))
    return string
