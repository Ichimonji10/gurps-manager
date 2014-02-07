"""Database schema for GURPS Manager.

It is possible to generate a diagram of the schema defined herein. See the
readme for details.

If a model does not specify a primary key, django automatically generates a
column named ``id``. Django will not generate ``id`` if you pass ``primary_key =
True`` to some other column.

"""
import re
from math import floor
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models

# pylint: disable=E1101
# no-member. Used when a variable is accessed for a nonexistent member.

def validate_not_negative(number):
    """Check whether ``number`` is positive.

    If check fails, raise a ``ValidationError``

    ``number`` can be a float or integer

    >>> from django.core.exceptions import ValidationError
    >>> validate_not_negative(0)
    >>> validate_not_negative(1)
    >>> validate_not_negative(5)
    >>> try:
    ...     validate_not_negative(-1)
    ... except ValidationError:
    ...     'an exception was raised'
    'an exception was raised'

    """
    if number < 0:
        raise ValidationError('{} is negative'.format(number))

def validate_quarter(number):
    """Check whether ``number`` is some multiple of 0.25.

    If check fails, raise a ``ValidationError``.

    ``number`` is a float.

    >>> from django.core.exceptions import ValidationError
    >>> validate_quarter(0.0)
    >>> validate_quarter(0.25)
    >>> validate_quarter(0.50)
    >>> try:
    ...     validate_quarter(0.26)
    ... except ValidationError:
    ...     'an exception was raised'
    'an exception was raised'

    """
    if Decimal(number).quantize(Decimal('0.01')) % Decimal(0.25) \
    != Decimal(0.00):
        raise ValidationError('{} is not divisible by 0.25.'.format(number))

class Campaign(models.Model):
    """A single role-playing campaign."""
    MAX_LEN_NAME = 50
    MAX_LEN_DESCRIPTION = 2000

    # many-to-many fields
    skillsets = models.ManyToManyField('SkillSet')

    # string-based fields
    name = models.CharField(max_length=MAX_LEN_NAME)
    description = models.TextField(
        max_length=MAX_LEN_DESCRIPTION,
        blank=True
    )

    def __str__(self):
        """Returns a string representation of the object"""
        return self.name

class SkillSet(models.Model):
    """A grouping of similar skills"""
    MAX_LEN_NAME = 50

    # string-based fields
    name = models.CharField(max_length=MAX_LEN_NAME)

    def __str__(self):
        """Returns a string representation of the object"""
        return self.name

class Character(models.Model):
    """An individual who can be role-played."""
    MAX_LEN_NAME = 50
    MAX_LEN_DESCRIPTION = 2000
    MAX_LEN_STORY = 2000
    APPEARANCE_CHOICES = (
        (-30, 'Horrific'),
        (-25, 'Monstrous'),
        (-20, 'Hideous'),
        (-10, 'Ugly'),
        (-5, 'Unattractive'),
        (0, 'Average'),
        (5, 'Attractive'),
        (15, 'Handsome/Beautiful'),
        (25, 'Very Handsome/Beautiful'),
        (35, 'Entrancing'),
    )
    WEALTH_CHOICES = (
        (-25, 'Dead Broke'),
        (-15, 'Poor'),
        (-10, 'Struggling'),
        (0, 'Average'),
        (10, 'Comfortable'),
        (20, 'Wealthy'),
        (30, 'Very Wealthy'),
        (50, 'Filthy Rich'),
    )
    EIDETIC_MEMORY_CHOICES = (
        (0, 'None'),
        (30, 'Partial'),
        (60, 'Full'),
    )
    MUSCLE_MEMORY_CHOICES = (
        (0, 'None'),
        (30, 'Partial'),
        (60, 'Full'),
    )

    # key fields
    campaign = models.ForeignKey(Campaign)

    # many-to-many fields
    skills = models.ManyToManyField('Skill', through='CharacterSkill', blank=True) # pylint: disable=C0301
    spells = models.ManyToManyField('Spell', through='CharacterSpell', blank=True) # pylint: disable=C0301
    items = models.ManyToManyField('Item', through='Possession', blank=True)

    # string-based fields
    name = models.CharField(max_length=MAX_LEN_NAME)
    description = models.TextField(max_length=MAX_LEN_DESCRIPTION, blank=True)
    story = models.TextField(max_length=MAX_LEN_STORY, blank=True)

    # integer fields
    strength = models.IntegerField(default=10, validators=[validate_not_negative]) # pylint: disable=C0301
    dexterity = models.IntegerField(default=10, validators=[validate_not_negative]) # pylint: disable=C0301
    intelligence = models.IntegerField(default=10, validators=[validate_not_negative]) # pylint: disable=C0301
    health = models.IntegerField(default=10, validators=[validate_not_negative])
    magery = models.IntegerField(default=0, validators=[validate_not_negative])
    bonus_fatigue = models.IntegerField(default=0)
    bonus_hitpoints = models.IntegerField(default=0)
    bonus_alertness = models.IntegerField(default=0)
    bonus_willpower = models.IntegerField(default=0)
    bonus_fright = models.IntegerField(default=0)
    bonus_speed = models.IntegerField(default=0)
    bonus_movement = models.IntegerField(default=0)
    bonus_dodge = models.IntegerField(default=0)
    bonus_initiative = models.IntegerField(default=0)
    free_strength = models.IntegerField(default=0)
    free_dexterity = models.IntegerField(default=0)
    free_intelligence = models.IntegerField(default=0)
    free_health = models.IntegerField(default=0)

    # float fields
    total_points = models.FloatField(validators=[validate_quarter])
    used_fatigue = models.FloatField(default=0, validators=[validate_quarter])

    # lookup fields
    appearance = models.IntegerField(choices=APPEARANCE_CHOICES, default=0)
    wealth = models.IntegerField(choices=WEALTH_CHOICES, default=0)
    eidetic_memory = models.IntegerField(
        choices=EIDETIC_MEMORY_CHOICES,
        default=0
    )
    muscle_memory = models.IntegerField(
        choices=MUSCLE_MEMORY_CHOICES,
        default=0
    )

    # derived fields
    def fatigue(self):
        """Returns a character's total fatigue"""
        return self.strength + self.bonus_fatigue

    def hitpoints(self):
        """Returns a character's total hitpoints"""
        return self.health + self.bonus_hitpoints

    def alertness(self):
        """Returns a character's alertness"""
        return self.intelligence + self.bonus_alertness

    def will(self):
        """Returns a character's will"""
        return self.intelligence + self.bonus_will

    def fright(self):
        """Returns a character's fright"""
        return self.intelligence + self.bonus_fright

    def initiative(self):
        """Returns a character's initiative"""
        return ((self.intelligence + self.dexterity) / 4) \
            + self.bonus_initiative

    def no_encumberance(self):
        """Returns a character's no encumberance upper limit"""
        return self.strength * 2

    def light_encumberance(self):
        """Returns a character's light encumberance upper limit"""
        return self.strength * 4

    def medium_encumberance(self):
        """Returns a character's medium encumberance upper limit"""
        return self.strength * 6

    def heavy_encumberance(self):
        """Returns a character's heavy encumberance upper limit"""
        return self.strength * 12

    def extra_heavy_encumberance(self):
        """Returns a character's extra heavy encumberance upper limit"""
        return self.strength * 20

    def total_possession_weight(self):
        """Returns the total weight of a character's possessions"""
        total_weight = 0
        for possession in Possession.objects.filter(character=self):
            total_weight += (possession.item.weight * possession.quantity)
        return total_weight

    def total_possession_value(self):
        """Returns the total value of a character's possessions"""
        total_cost = 0
        for possession in Possession.objects.filter(character=self):
            total_cost += (possession.item.cost * possession.quantity)
        return total_cost

    def encumberance_penalty(self):
        """Returns the encumberance penalty incurred by a character's total
        possession weight.

        """
        if self.total_possession_weight() < self.no_encumberance:
            return 0
        elif self.total_possession_weight() < self.light_encumberance:
            return 1
        elif self.total_possession_weight() < self.medium_encumberance:
            return 2
        elif self.total_possession_weight() < self.heavy_encumberance:
            return 3
        elif self.total_possession_weight() < self.extra_heavy_encumberance:
            return 4
        else:
            # TODO figure out whether this is how I actually want to handle
            # over-encumberance
            return 10000

    def speed(self):
        """Returns a character's speed"""
        for skill in CharacterSkill.objects.filter(character=self):
            if re.search('^running$', skill.skill.name, flags=re.IGNORECASE):
                return ((self.dexterity + self.health) / 4) \
                    + (skill.score() / 8) \
                    + self.bonus_speed
        return ((self.dexterity + self.health) / 4) + self.bonus_speed

    def movement(self):
        """Returns a character's movement"""
        return floor(self.speed()) \
            - self.encumberance_penalty() \
            + self.bonus_movement

    def dodge(self):
        """Returns a character's speed"""
        return floor(self.speed()) \
            - self.encumberance_penalty() \
            + self.bonus_dodge

    def points_in_strength(self):
        """Returns the points a character has spent in strength"""
        return self._points_in_attribute(self.strength)

    def points_in_dexterity(self):
        """Returns the points a character has spent in dexterity"""
        return self._points_in_attribute(self.dexterity)

    def points_in_intelligence(self):
        """Returns the points a character has spent in intelligence"""
        return self._points_in_attribute(self.intelligence)

    def points_in_health(self):
        """Returns the points a character has spent in health"""
        return self._points_in_attribute(self.health)

    def _points_in_attribute(self, level):
        """Returns the points required to achieve the given level of an attribute

        For reference of where all these magic numbers come from, see:
            GURPS Basic Set 3rd Edition Revised, page 13
        """
        if(8 > level):
            return (9 - level) * -10
        elif(9 > level):
            return -15
        elif(14 > level):
            return (level - 10) * 10
        elif(15 > level):
            return 45
        elif(18 > level):
            return (level - 12) * 20
        else:
            return (level - 13) * 25

    def total_points_in_attributes(self):
        """Returns the points a character has spent in attributes"""
        return self.points_in_strength() \
                + self.points_in_dexterity() \
                + self.points_in_intelligence() \
                + self.points_in_health()

    def total_points_in_skills(self):
        """Returns the points a character has spent in skills"""
        total_points = 0
        for skill in CharacterSkill.objects.filter(character=self):
            total_points += skill.points
        return total_points

    def total_points_in_spells(self):
        """Returns the points a character has spent in spells"""
        total_points = 0
        for spell in CharacterSpell.objects.filter(character=self):
            total_points += spell.points
        return total_points

    def total_points_in_advantages(self):
        """Returns the points a character has spent in advantages"""
        total_points = 0
        for trait in Trait.objects.filter(character=self):
            if trait.points > 0:
                total_points += trait.points
        return total_points

    def total_points_in_disadvantages(self):
        """Returns the points a character has spent in disadvantages"""
        total_points = 0
        for trait in Trait.objects.filter(character=self):
            if trait.points < 0:
                total_points += trait.points
        return total_points

    def total_points_in_special_traits(self):
        """Returns the points a character has spent in special traits"""
        return self.eidetic_memory \
            + self.muscle_memory \
            + self.wealth \
            + self.appearance

    def total_character_points_spent(self):
        """Returns the points a character has spent in total"""
        return self.total_points_in_attributes() \
            + self.total_points_in_advantages() \
            + self.total_points_in_disadvantages() \
            + self.total_points_in_skills() \
            + self.total_points_in_spells() \
            + self.total_points_in_special_traits()

    def __str__(self):
        """Returns a string representation of the object"""
        return self.name

class Trait(models.Model):
    """An Advantage or Disadvantage that a character may have"""
    MAX_LEN_NAME = 50
    MAX_LEN_DESCRIPTION = 2000

    # key fields
    character = models.ForeignKey(Character)

    # string-based fields
    name = models.CharField(max_length=MAX_LEN_NAME)
    description = models.TextField(max_length=MAX_LEN_DESCRIPTION, blank=True)

    # float fields
    points = models.FloatField(validators=[validate_quarter])

    def __str__(self):
        """Returns a string representation of the object"""
        return self.name

class Skill(models.Model):
    """A skill available to characters.

    A skill is some task that a character has some proficency in. For example, a
    character could become proficent in dagger throwing or underwater basket
    weaving.

    """
    MAX_LEN_NAME = 50
    CATEGORY_CHOICES = (
        (1, 'Mental'),
        (2, 'Mental (health)'),
        (3, 'Physical'),
        (4, 'Physical (health)'),
        (5, 'Physical (strength'),
    )
    DIFFICULTY_CHOICES = (
        (1, 'Easy'),
        (2, 'Average'),
        (3, 'Hard'),
        (4, 'Very Hard'),
    )

    # key fields
    skillset = models.ForeignKey(SkillSet)

    # string-based fields
    name = models.CharField(max_length=MAX_LEN_NAME)

    # lookup fields
    category = models.IntegerField(choices=CATEGORY_CHOICES)
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES)

    def __str__(self):
        """Returns a string representation of the object"""
        return self.name

class CharacterSkill(models.Model):
    """A skill that a character possesses"""
    # key fields
    skill = models.ForeignKey(Skill)
    character = models.ForeignKey(Character)

    # integer fields
    bonus_level = models.IntegerField(default=0)

    # float fields
    points = models.FloatField(validators=[validate_quarter], default=0)

    def score(self):
        """Returns a character's score in a given skill"""
        effective_points_physical = self.points * (
            1 if self.character.muscle_memory == 0
            else (self.character.muscle_memory / 15)
        )
        effective_points_mental = self.points * (
            1 if self.character.eidetic_memory == 0
            else (self.character.eidetic_memory / 15)
        )

        # intelligence based mental skill
        if self.skill.category == 1:
            if effective_points_mental < 0.5:
                return 0
            elif effective_points_mental < 1:
                return self.character.intelligence - self.skill.difficulty
            elif effective_points_mental < 2:
                return self.character.intelligence - self.skill.difficulty + 1
            elif effective_points_mental < 4:
                return self.character.intelligence - self.skill.difficulty + 2
            else:
                if self.skill.difficulty < 4:
                    return self.character.intelligence \
                        - self.skill.difficulty \
                        + (effective_points_mental // 2) + 1
                else:
                    return self.character.intelligence \
                        - self.skill.difficulty \
                        + (effective_points_mental // 4) + 2

        # health based mental skill
        elif self.skill.category == 2:
            if effective_points_mental < 0.5:
                return 0
            elif effective_points_mental < 1:
                return self.character.health - self.skill.difficulty
            elif effective_points_mental < 2:
                return self.character.health - self.skill.difficulty + 1
            elif effective_points_mental < 4:
                return self.character.health - self.skill.difficulty + 2
            else:
                if self.skill.difficulty < 4:
                    return self.character.health \
                        - self.skill.difficulty \
                        + (effective_points_mental // 2) + 1
                else:
                    return self.character.health \
                        - self.skill.difficulty \
                        + (effective_points_mental // 4) + 2

        # dexterity based physical skill
        elif self.skill.category == 3:
            if effective_points_physical < 0.5:
                return 0
            elif effective_points_physical < 1:
                return self.character.dexterity - self.skill.difficulty
            elif effective_points_physical < 2:
                return self.character.dexterity - self.skill.difficulty + 1
            elif effective_points_physical < 4:
                return self.character.dexterity - self.skill.difficulty + 2
            elif effective_points_physical < 8:
                return self.character.dexterity - self.skill.difficulty + 3
            else:
                return self.character.dexterity - self.skill.difficulty \
                    + (effective_points_physical // 8) + 3

        # health based physical skill
        elif self.skill.category == 4:
            if effective_points_physical < 0.5:
                return 0
            elif effective_points_physical < 1:
                return self.character.health - self.skill.difficulty
            elif effective_points_physical < 2:
                return self.character.health - self.skill.difficulty + 1
            elif effective_points_physical < 4:
                return self.character.health - self.skill.difficulty + 2
            elif effective_points_physical < 8:
                return self.character.health - self.skill.difficulty + 3
            else:
                return self.character.health \
                    - self.skill.difficulty \
                    + (effective_points_physical // 8) + 3

        # strength based physical skill
        elif self.skill.category == 5:
            if effective_points_physical < 0.5:
                return 0
            elif effective_points_physical < 1:
                return self.character.strength - self.skill.difficulty
            elif effective_points_physical < 2:
                return self.character.strength - self.skill.difficulty + 1
            elif effective_points_physical < 4:
                return self.character.strength - self.skill.difficulty + 2
            elif effective_points_physical < 8:
                return self.character.strength - self.skill.difficulty + 3
            else:
                return self.character.strength \
                    - self.skill.difficulty \
                    + (effective_points_physical // 8) + 3

        # TODO add exception handling for this case, it should never really
        # occur
        else:
            return 0

class Spell(models.Model):
    """A Spell available to characters

    Anything from fireballs to feather falling

    """
    MAX_LEN_NAME = 50
    MAX_LEN_SCHOOL = 50
    MAX_LEN_RESIST = 50
    DIFFICULTY_CHOICES = (
        (3, 'Hard'),
        (4, 'Very Hard'),
    )

    # string-based fields
    name = models.CharField(max_length=MAX_LEN_NAME)
    school = models.CharField(max_length=MAX_LEN_SCHOOL)
    resist = models.CharField(max_length=MAX_LEN_RESIST)

    # integer fields
    cast_time = models.IntegerField()
    duration = models.IntegerField()
    initial_fatigue_cost = models.IntegerField()
    maintainance_fatigue_cost = models.IntegerField()

    # lookup fields
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES)

    def __str__(self):
        """Returns a string representation of the object"""
        return self.name

class CharacterSpell(models.Model):
    """A spell that a character may know"""
    # key fields
    spell = models.ForeignKey(Spell)
    character = models.ForeignKey(Character)

    # integer fields
    bonus_level = models.IntegerField(default=0)

    # float fields
    points = models.FloatField(validators=[validate_quarter], default=0)

    def score(self):
        eidetic_memory_factor = self.character.eidetic_memory / 30
        if self.points < 0.5:
            return 0
        elif self.points < 1:
            return self.character.intelligence \
                - self.skill.difficulty \
                + eidetic_memory_factor
        elif self.points < 2:
            return self.character.intelligence \
                - self.skill.difficulty + 1 \
                + eidetic_memory_factor
        elif self.points < 4:
            return self.character.intelligence \
                - self.skill.difficulty + 2 \
                + eidetic_memory_factor
        else:
            if self.skill.difficulty < 4:
                return self.character.intelligence \
                    - self.skill.difficulty \
                    + (self.points // 2) \
                    + 1 + eidetic_memory_factor
            else:
                return self.character.intelligence \
                    - self.skill.difficulty \
                    + (self.points // 4) \
                    + 2 + eidetic_memory_factor

class Item(models.Model):
    """An item that a character may possess"""
    MAX_LEN_NAME = 50
    MAX_LEN_DESCRIPTION = 2000

    # string-based fields
    name = models.CharField(max_length=MAX_LEN_NAME)
    description = models.TextField(max_length=MAX_LEN_DESCRIPTION, blank=True)

    # float fields
    cost = models.FloatField(validators=[validate_not_negative])
    weight = models.FloatField(validators=[validate_not_negative])

    def __str__(self):
        """Returns a string representation of the object"""
        return self.name

class Possession(models.Model):
    """An item that a character possesses"""
    # key fields
    item = models.ForeignKey(Item)
    character = models.ForeignKey(Character)

    # integer fields
    quantity = models.IntegerField(validators=[validate_not_negative])

class HitLocation(models.Model):
    """A location on a character that can be affected

    Affectations include: armor value, damage, status effects, etc.

    """
    MAX_LEN_NAME = 50
    MAX_LEN_STATUS = 500

    # key fields
    character = models.ForeignKey(Character)

    # string-based fields
    name = models.CharField(max_length=MAX_LEN_NAME)
    status = models.TextField(max_length=MAX_LEN_STATUS, blank=True)

    # integer fields
    passive_damage_resistance = models.IntegerField()
    damage_resistance = models.IntegerField()
    damage_taken = models.IntegerField(default=0)

    def __str__(self):
        """Returns a string representation of the object"""
        return self.name
