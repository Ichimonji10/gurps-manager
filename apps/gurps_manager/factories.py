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
    name = FuzzyAttribute(lambda: character_name()) # pylint: disable=W0108

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
