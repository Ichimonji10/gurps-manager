"""Database schema for GURPS Manager.

It is possible to generate a diagram of the schema defined herein. See the
readme for details.

If a model does not specify a primary key, django automatically generates a
column named ``id``. Django will not generate ``id`` if you pass ``primary_key =
True`` to some other column.

"""
from django.db import models

# pylint: disable=R0903
# "Too few public methods (0/2)"
# It is both common and OK for a model to have no methods.
#
# pylint: disable=W0232
# "Class has no __init__ method"
# It is both common and OK for a model to have no __init__ method.

class Character(models.Model):
    """An individual who can be role-played."""
    MAX_LEN_NAME = 50
    MAX_LEN_DESCRIPTION = 2000
    MAX_LEN_STORY = 2000

    name = models.CharField(max_length = MAX_LEN_NAME)
    description = models.TextField(
        max_length = MAX_LEN_DESCRIPTION,
        blank = True
    )
    story = models.CharField(
        max_length = MAX_LEN_STORY,
        blank = True
    )
    """If possible, this should be limited to 2 decimal places"""
    total_points = models.FloatField() 
    strength = models.IntegerField()
    dexterity = models.IntegerField()
    intelligence = models.IntegerField()
    health = models.IntegerField()
    appearance = models.IntegerField()
    wealth = models.IntegerField()
    magery = models.IntegerField()
    eidetic_memory = models.IntegerField()
    used_fatigue = models.FloatField()
    bonus_fatigue = models.IntegerField()
    bonus_hitpoints = models.IntegerField()
    bonus_alertness = models.IntegerField()
    bonus_willpower = models.IntegerField()
    bonus_fright = models.IntegerField()
    bonus_speed = models.IntegerField()
    bonus_movement = models.IntegerField()
    bonus_dodge = models.IntegerField()
    bonus_initiative = models.IntegerField()
    free_strength = models.IntegerField()
    free_dexterity = models.IntegerField()
    free_intelligence = models.IntegerField()
    free_health = models.IntegerField()
    
    
    
