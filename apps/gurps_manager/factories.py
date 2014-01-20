"""Factory Boy factory definitions.

These factory definitions are used as an alternative to plain old Django
fixtures. Rather than simply defining a static set of test data, factories can
be used to generate disgustingly random data. (perfect for testing!)

"""
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyAttribute
from gurps_manager import models
import random

class CharacterFactory(DjangoModelFactory):
    """Instantiate an ``gurps_manager.models.Character`` object.

    >>> CharacterFactory.build().full_clean()
    >>> CharacterFactory.create().id is None
    False

    """
    # pylint: disable=R0903
    # pylint: disable=W0232
    FACTORY_FOR = models.Character
    name = FuzzyAttribute(lambda: character_name()) # pylint: disable=W0108

    # integer-based fields
    strength = FuzzyAttribute(lambda: character_intfield())
    dexterity = FuzzyAttribute(lambda: character_intfield())
    intelligence = FuzzyAttribute(lambda: character_intfield())
    health = FuzzyAttribute(lambda: character_intfield())
    appearance = FuzzyAttribute(lambda: character_intfield())
    wealth = FuzzyAttribute(lambda: character_intfield())
    magery = FuzzyAttribute(lambda: character_intfield())
    eidetic_memory = FuzzyAttribute(lambda: character_intfield())
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
    # FIXME: what are valid ranges for these values? Should separate methods be
    # created for each of a character's attributes?
    return random.randint(0, 100)

def character_floatfield():
    """Return a value for an float-based ``Character`` model attribute.

    >>> isinstance(character_floatfield(), float)
    True

    """
    # FIXME: what are valid ranges for these values? Should separate methods be
    # created for each of a character's attributes?
    return 0.25 * random.randint(0, 400)

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
    if(lower >= upper):
        return lower
    return random.randint(0, upper - lower) + lower

def _random_str(min_len = 0, max_len = 0):
    """Return a string consisting of random UTF-8 characters.

    If ``min_len >= max_len``, return a string exactly ``min_len`` characters
    long. Otherwise, return a string between ``min_len`` and ``max_len`` chars
    long, inclusive.

    See also: http://docs.python.org/3/library/functions.html#chr

    """
    string = ''
    for i in range(_random_int(min_len, max_len)):
        string += chr(random.randrange(0, 0x10FFFF))
    return string
