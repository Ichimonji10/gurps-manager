"""Database schema for GURPS Manager.

It is possible to generate a diagram of the schema defined herein. See the
readme for details.

If a model does not specify a primary key, django automatically generates a
column named ``id``. Django will not generate ``id`` if you pass ``primary_key =
True`` to some other column.

"""
from decimal import Decimal
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from math import floor
import re

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

    # key fields
    owner = models.ForeignKey(User)

    # many-to-many fields
    skillsets = models.ManyToManyField('SkillSet', blank=True)

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
    # pylint: disable=R0904
    # GURPS has an enormous number of derived fields on its characters
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
    owner = models.ForeignKey(User)

    # many-to-many fields
    skills = models.ManyToManyField('Skill', through='CharacterSkill', blank=True) # pylint: disable=C0301
    spells = models.ManyToManyField('Spell', through='CharacterSpell', blank=True) # pylint: disable=C0301
    items = models.ManyToManyField('Item', through='Possession', blank=True)

    # string-based fields
    name = models.CharField(max_length=MAX_LEN_NAME, default='New Character')
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
        return self.intelligence + self.bonus_willpower

    def fright(self):
        """Returns a character's fright"""
        return self.intelligence + self.bonus_fright

    def initiative(self):
        """Returns a character's initiative"""
        return ((self.intelligence + self.dexterity) / 4) \
            + self.bonus_initiative

    def no_encumbrance(self):
        """Returns a character's no encumbrance upper limit"""
        return self.strength * 2

    def light_encumbrance(self):
        """Returns a character's light encumbrance upper limit"""
        return self.strength * 4

    def medium_encumbrance(self):
        """Returns a character's medium encumbrance upper limit"""
        return self.strength * 6

    def heavy_encumbrance(self):
        """Returns a character's heavy encumbrance upper limit"""
        return self.strength * 12

    def extra_heavy_encumbrance(self):
        """Returns a character's extra heavy encumbrance upper limit"""
        return self.strength * 20

    def total_possession_weight(self):
        """Returns the total weight of a character's possessions"""
        total_weight = 0
        for possession in Possession.objects.filter(character=self):
            total_weight += (possession.item.weight * possession.quantity)
        return total_weight

    def total_possession_value(self):
        """Returns the total value of a character's possessions"""
        total_value = 0
        for possession in Possession.objects.filter(character=self):
            total_value += (possession.item.value * possession.quantity)
        return total_value

    def encumbrance_penalty(self):
        """Returns the movement penalty incurred by a character's total
        possession weight (encumbrance).

        For reference of where all these magic numbers come from, see:
            GURPS Basic Set 3rd Edition Revised, page 76

        """
        if self.total_possession_weight() < self.no_encumbrance():
            return 0
        elif self.total_possession_weight() < self.light_encumbrance():
            return 1
        elif self.total_possession_weight() < self.medium_encumbrance():
            return 2
        elif self.total_possession_weight() < self.heavy_encumbrance():
            return 3
        elif self.total_possession_weight() < self.extra_heavy_encumbrance():
            return 4
        else:
            # Returns a penatly such that the character's movement will be -1
            # This indicates over encumbrance
            return floor(self.speed()) + self.bonus_movement + 1

    def speed(self):
        """Returns a character's speed"""
        return ((self.dexterity + self.health) / 4) + self.bonus_speed

    def movement(self):
        """Returns a character's movement"""
        # Factor in the running skill if they have it.
        running_bonus = 0
        for skill in CharacterSkill.objects.filter(character=self):
            if re.search('^running$', skill.skill.name, flags=re.IGNORECASE):
                running_bonus = (skill.score() / 8)
        return floor(self.speed() + running_bonus) \
            - self.encumbrance_penalty() \
            + self.bonus_movement

    def dodge(self):
        """Returns a character's speed"""
        return floor(self.speed()) \
            - self.encumbrance_penalty() \
            + self.bonus_dodge

    def points_in_strength(self):
        """Returns the points a character has spent in strength"""
        return self._points_in_attribute(self.strength - self.free_strength)

    def points_in_dexterity(self):
        """Returns the points a character has spent in dexterity"""
        return self._points_in_attribute(self.dexterity - self.free_dexterity)

    def points_in_intelligence(self):
        """Returns the points a character has spent in intelligence"""
        return self._points_in_attribute(
            self.intelligence - self.free_intelligence
        )

    def points_in_health(self):
        """Returns the points a character has spent in health"""
        return self._points_in_attribute(self.health - self.free_health)

    @classmethod
    def _points_in_attribute(cls, level):
        """Returns the points required to achieve the given level of an
        attribute

        For reference of where all these magic numbers come from, see:
            GURPS Basic Set 3rd Edition Revised, page 13

        """
        if 8 > level:
            return (9 - level) * -10
        elif 9 > level:
            return -15
        elif 14 > level:
            return (level - 10) * 10
        elif 15 > level:
            return 45
        elif 18 > level:
            return (level - 12) * 20
        else:
            return (level - 13) * 25

    def points_in_magery(self):
        """Returns the points a character has spent in magery"""
        if self.magery == 0:
            return 0
        else:
            return (self.magery * 10) + 5

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
            + self.appearance \
            + self.points_in_magery()

    def total_points_spent(self):
        """Returns the points a character has spent in total"""
        return self.total_points_in_attributes() \
            + self.total_points_in_advantages() \
            + self.total_points_in_disadvantages() \
            + self.total_points_in_skills() \
            + self.total_points_in_spells() \
            + self.total_points_in_special_traits()

    def points_remaining(self):
        """Returns the points a character has left to spend"""
        return self.total_points - self.total_points_spent()

    def __str__(self):
        """Returns a string representation of the object"""
        return self.name

    def clean(self):
        """Perform model-wide validation."""
        # Don't allow the user to spend too many character points.
        try:
            if self.total_points_spent() > self.total_points:
                raise ValidationError(
                    'Too many character points spent. Only {} are available; '
                    'you spent {}.'.format(
                        self.total_points,
                        self.total_points_spent()
                    )
                )
        except TypeError:
            # This error occurs if, say, total_points_spent is 150 and
            # total_points is None.
            raise ValidationError(
                'Could not check if too many character points have been spent. '
                'Have you set "total points" yet?'
            )

class Trait(models.Model):
    """An Advantage or Disadvantage that a character may have"""
    MAX_LEN_NAME = 50
    MAX_LEN_DESCRIPTION = 2000

    # key fields
    character = models.ForeignKey(Character)

    # string-based fields
    name = models.CharField(max_length=MAX_LEN_NAME)
    description = models.TextField(max_length=MAX_LEN_DESCRIPTION, blank=True)

    # integer fields
    points = models.IntegerField()

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
        (5, 'Physical (strength)'),
        (6, 'Psionic')
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

    @classmethod
    def get_category_id(cls, name):
        """Given a name from ``CATEGORY_CHOICES``, return its ID.

        >>> Skill.get_category_id('Mental')
        1
        >>> Skill.get_category_id('Psionic')
        6

        """
        return _get_choice_id(cls.CATEGORY_CHOICES, name)

class CharacterSkill(models.Model):
    """A skill that a character possesses"""
    MAX_LEN_COMMENTS = 50

    # key fields
    skill = models.ForeignKey(Skill)
    character = models.ForeignKey(Character)

    # string-based fields
    comments = models.CharField(max_length=MAX_LEN_COMMENTS, blank=True)

    # integer fields
    bonus_level = models.IntegerField(default=0)

    # float fields
    points = models.FloatField(validators=[validate_quarter], default=0)

    def score(self):
        """Returns a character's score in a given skill

        For reference of where all these magic numbers come from, see:
            GURPS Basic Set 3rd Edition Revised, page 44

        """
        # intelligence based mental skill
        if self.skill.category == Skill.get_category_id('Mental'):
            return self._mental_skill_score(self.character.intelligence)

        # health based mental skill
        elif self.skill.category == Skill.get_category_id('Mental (health)'):
            return self._mental_skill_score(self.character.health)

        # dexterity based physical skill
        elif self.skill.category == Skill.get_category_id('Physical'):
            return self._physical_skill_score(self.character.dexterity)

        # health based physical skill
        elif self.skill.category == Skill.get_category_id('Physical (health)'):
            return self._physical_skill_score(self.character.health)

        # strength based physical skill
        elif self.skill.category == Skill.get_category_id('Physical (strength)'): # pylint: disable=C0301
            return self._physical_skill_score(self.character.strength)

        # psionic skill
        elif self.skill.category == Skill.get_category_id('Psionic'):
            return self._psionic_skill_score()

        else:
            raise ValueError("The category referenced is outside the known set")

    def _effective_points_mental(self):
        """Calculate effective mental points.

        >>> from gurps_manager import factories
        >>> character_skill = factories.CharacterSkillFactory.create()
        >>> isinstance(character_skill._effective_points_mental(), float)
        True

        """
        return self.points * (
            1 if self.character.eidetic_memory == 0
            else (self.character.eidetic_memory / 15)
        )

    def _mental_skill_score(self, attribute):
        """Calculates the score of a mental skill with a given base attribute"""
        effective_points_mental = self._effective_points_mental()
        base_score = attribute - self.skill.difficulty
        if effective_points_mental < 0.5:
            return 0
        elif effective_points_mental < 1:
            return base_score
        elif effective_points_mental < 2:
            return base_score + 1
        elif effective_points_mental < 4:
            return base_score + 2
        elif self.skill.difficulty < 4:
            return base_score + (effective_points_mental // 2) + 1
        else:
            return base_score + (effective_points_mental // 4) + 2

    def _effective_points_physical(self):
        """Calculate effective physical points.

        >>> from gurps_manager import factories
        >>> character_skill = factories.CharacterSkillFactory.create()
        >>> isinstance(character_skill._effective_points_physical(), float)
        True

        """
        return self.points * (
            1 if self.character.muscle_memory == 0
            else (self.character.muscle_memory / 15)
        )

    def _physical_skill_score(self, attribute):
        """Calculates the score of a mental skill with a given base attribute"""
        effective_points_physical = self._effective_points_physical()
        base_score = attribute - self.skill.difficulty
        if effective_points_physical < 0.5:
            return 0
        elif effective_points_physical < 1:
            return base_score
        elif effective_points_physical < 2:
            return base_score + 1
        elif effective_points_physical < 4:
            return base_score + 2
        elif effective_points_physical < 8:
            return base_score + 3
        else:
            return base_score + (effective_points_physical // 8) + 3

    def _psionic_skill_score(self):
        """Calculates the score of a mental skill with a given base attribute"""
        base_score = self.character.intelligence - self.skill.difficulty
        if self.points < 0.5:
            return 0
        elif self.points < 1:
            return base_score
        elif self.points < 2:
            return base_score + 1
        elif self.points < 4:
            return base_score + 2
        elif self.skill.difficulty < 4:
            return base_score + (self.points // 2) + 1
        else:
            return base_score + (self.points // 4) + 2

class Spell(models.Model):
    """A Spell available to characters

    Anything from fireballs to feather falling

    """
    MAX_LEN_NAME = 50
    MAX_LEN_SCHOOL = 50
    MAX_LEN_RESIST = 50
    MAX_LEN_DURATION = 50
    DIFFICULTY_CHOICES = (
        (3, 'Hard'),
        (4, 'Very Hard'),
    )

    # key fields
    campaign = models.ForeignKey(Campaign)

    # string-based fields
    name = models.CharField(max_length=MAX_LEN_NAME)
    school = models.CharField(max_length=MAX_LEN_SCHOOL)
    resist = models.CharField(max_length=MAX_LEN_RESIST)
    duration = models.CharField(max_length=MAX_LEN_DURATION)

    # integer fields
    cast_time = models.IntegerField(validators=[validate_not_negative])
    initial_fatigue_cost = models.IntegerField(
        validators=[validate_not_negative], verbose_name='IFC'
    )
    maintenance_fatigue_cost = models.IntegerField(
        validators=[validate_not_negative], verbose_name='MFC'
    )

    # lookup fields
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES)

    def __str__(self):
        """Returns a string representation of the object"""
        return self.name

    @classmethod
    def get_difficulty_id(cls, name):
        """Given a name from ``DIFFICULTY_CHOICES``, return its ID.

        >>> Spell.get_difficulty_id('Hard')
        3
        >>> Spell.get_difficulty_id('Very Hard')
        4

        """
        return _get_choice_id(cls.DIFFICULTY_CHOICES, name)

class CharacterSpell(models.Model):
    """A spell that a character may know"""
    # key fields
    spell = models.ForeignKey(Spell)
    character = models.ForeignKey(Character)

    # integer fields
    bonus_level = models.IntegerField(default=0)

    # float fields
    points = models.FloatField(validators=[validate_quarter], default=0)

    def _base_score(self):
        """Return a base score used to calculate an actual score.

        >>> from gurps_manager.factories import CharacterSpellFactory
        >>> character_spell = CharacterSpellFactory.build()
        >>> isinstance(character_spell._base_score(), int)
        True

        """
        eidetic_memory_factor = self.character.eidetic_memory // 30
        return self.character.intelligence \
            + self.character.magery \
            - self.spell.difficulty \
            + eidetic_memory_factor

    def score(self):
        """Returns a character's score in a given spell

        For reference of where all these magic numbers come from, see:
            GURPS Basic Set 3rd Edition Revised, page 44
            (spells are simply a special subset of skills)

        """
        base_score = self._base_score()
        if self.points < 0.5:
            return 0
        elif self.points < 1:
            return base_score
        elif self.points < 2:
            return base_score + 1
        elif self.points < 4:
            return base_score + 2
        elif self.spell.difficulty < 4:
            # self.points >= 4
            return base_score + (self.points // 2) + 1
        else:
            # self.points >= 4 and self.spell.difficulty >= 4
            return base_score + (self.points // 4) + 2

class Item(models.Model):
    """An item that a character may possess"""
    MAX_LEN_NAME = 50
    MAX_LEN_DESCRIPTION = 2000

    # key fields
    campaign = models.ForeignKey(Campaign)

    # string-based fields
    name = models.CharField(max_length=MAX_LEN_NAME)
    description = models.TextField(max_length=MAX_LEN_DESCRIPTION, blank=True)

    # float fields
    value = models.FloatField(validators=[validate_not_negative])
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
    passive_defense = models.IntegerField(verbose_name='PD')
    damage_resistance = models.IntegerField(verbose_name='DR')
    damage_taken = models.IntegerField(default=0)

    def __str__(self):
        """Returns a string representation of the object"""
        return self.name

def _get_choice_id(choices, choice_name):
    """Given a name from ``choices``, return its ID.

    ``choices`` is a tuple of tuples.

    >>> choices = ((1, 'foo'), (2, 'bar'), (42, 'biz'))
    >>> _get_choice_id(choices, 'foo')
    1
    >>> _get_choice_id(choices, 'bar')
    2
    >>> _get_choice_id(choices, 'biz')
    42

    """
    # e.g. ['foo', 'bar', 'biz']
    choice_names = [choice[1] for choice in choices]
    # e.g. (1, 'foo')
    choice = choices[choice_names.index(choice_name)]
    return choice[0]
