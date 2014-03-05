"""Forms for creating and updating objects.

Unless otherwise noted, all forms defined herein can be used to either create or
update an object.

"""
from django.forms import ModelForm
from gurps_manager import models

# pylint: disable=R0903
# "Too few public methods (0/2)"
# It is both common and OK for a form to have no methods.
#
# pylint: disable=W0232
# "Class has no __init__ method"
# It is both common and OK for a form to have no __init__ method.

class CampaignForm(ModelForm):
    """A form for a Campaign."""

    class Meta(object):
        """Form attributes that are not custom fields."""
        model = models.Campaign
        fields = ['name', 'description', 'skillsets']

class CharacterForm(ModelForm):
    """A form for creating and editing a Character."""

    class Meta(object):
        """Form attributes that are not custom fields."""
        model = models.Character
        exclude = ['skills', 'spells', 'items']
        # There are a lot of attributes on the Character model, and we want to
        # display them all. If we want to display only some fields, use `fields`
        # or `exclude`.

class CharacterSkillForm(ModelForm):
    """A form for creating and editing a CharacterSkill."""

    class Meta(object):
        """Form attributes that are not custom fields."""
        model = models.CharacterSkill

class CharacterSpellForm(ModelForm):
    """A form for creating and editing a CharacterSpell."""

    class Meta(object):
        """Form attributes that are not custom fields."""
        model = models.CharacterSpell

class PossessionForm(ModelForm):
    """A form for creating and editing a Possession."""

    class Meta(object):
        """Form attributes that are not custom fields."""
        model = models.Possession
