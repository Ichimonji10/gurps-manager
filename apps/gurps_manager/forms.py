"""Forms for creating and updating objects.

Unless otherwise noted, all forms defined herein can be used to either create or
update an object.

"""
from django.forms import CharField, Form, ModelChoiceField, ModelForm, widgets
from django.forms.models import inlineformset_factory
from gurps_manager import models

# pylint: disable=R0903
# "Too few public methods (0/2)"
# It is both common and OK for a form to have no methods.
#
# pylint: disable=W0232
# "Class has no __init__ method"
# It is both common and OK for a form to have no __init__ method.

class LoginForm(Form):
    """A form for logging in a user."""
    username = CharField()
    password = CharField(widget=widgets.PasswordInput)

    class Meta(object):
        """Form attributes that are not fields."""
        fields = ['username', 'password']

class CampaignForm(ModelForm):
    """A form for a Campaign."""

    class Meta(object):
        """Form attributes that are not custom fields."""
        model = models.Campaign
        fields = ['name', 'description', 'skillsets', 'owner']

class CharacterForm(ModelForm):
    """A form for creating and editing a Character."""

    class Meta(object):
        """Form attributes that are not custom fields."""
        model = models.Character
        exclude = ['skills', 'spells', 'items']
        # There are a lot of attributes on the Character model, and we want to
        # display them all. If we want to display only some fields, use `fields`
        # or `exclude`.

def character_skill_form(character):
    """Generate a form class for ``CharacterSkill`` objects.

    ``character`` is a ``Character`` model object.

    The form class returned is suitable for creating, editing and deleting
    ``CharacterSkill``s belonging to character ``character``. Not all skills can
    be assigned to ``character``. Instead, a skill will only be available if
    that skill's skillset belongs to ``character``'s campaign.

    >>> from gurps_manager import factories
    >>> from django.forms.models import ModelForm
    >>> character = factories.CharacterFactory.create()
    >>> formset_cls = character_skill_form(character)
    >>> formset_cls.__name__
    'CharacterSkillForm'
    >>> ModelForm in formset_cls.__bases__
    True

    """
    class CharacterSkillForm(ModelForm):
        """A form for creating or editing a ``CharacterSkill`` object."""
        skill = ModelChoiceField(
            queryset=models.Skill.objects.filter( # pylint: disable=E1101
                skillset__in=character.campaign.skillsets.values_list('id', flat=True) # pylint: disable=C0301
            )
        )

        class Meta(object):
            """Form attributes that are not custom fields."""
            model = models.CharacterSkill

    return CharacterSkillForm

def character_skill_formset(character):
    """Generate an inline formset class for ``CharacterSkill`` objects.

    ``character`` is a ``Character`` model object.

    The inline formset can be used to edit ``CharacterSkill`` objects belonging
    to ``character``. For details on how each individual form in the inline
    formset behaves, see the documentation for function
    ``character_skill_form``.

    """
    return inlineformset_factory(
        models.Character,
        models.CharacterSkill,
        extra=5,
        form=character_skill_form(character)
    )

def character_spell_form(character):
    """Generate a form class for ``CharacterSkill`` objects.

    ``character`` is a ``Character`` model object.

    The form class returned is suitable for creating, editing and deleting
    ``CharacterSpell``s belonging to character ``character``. Not all spells can
    be assigned to ``character``. Instead, a spell will only be available if
    that spell belongs to ``character``'s campaign.

    >>> from gurps_manager import factories
    >>> from django.forms.models import ModelForm
    >>> character = factories.CharacterFactory.create()
    >>> formset_cls = character_spell_form(character)
    >>> formset_cls.__name__
    'CharacterSpellForm'
    >>> ModelForm in formset_cls.__bases__
    True

    """
    class CharacterSpellForm(ModelForm):
        """A form for creating or editing a ``CharacterSpell`` object."""
        spell = ModelChoiceField(
            queryset=models.Spell.objects.filter( # pylint: disable=E1101
                campaign=character.campaign
            )
        )

        class Meta(object):
            """Form attributes that are not custom fields."""
            model = models.CharacterSpell

    return CharacterSpellForm

def character_spell_formset(character):
    """Generate an inline formset class for ``CharacterSpell`` objects.

    The inline formset class can be used to edit ``CharacterSpell`` objects
    belonging to a particular ``Character`` object.

    """
    return inlineformset_factory(
        models.Character,
        models.CharacterSpell,
        extra=5,
        form=character_skill_form(character)
    )

def possession_form(character):
    """Generate a form class for ``Possession`` objects.

    ``character`` is a ``Character`` model object.

    The form class returned is suitable for creating, editing and deleting
    ``Possession``s belonging to character ``character``. Not all items can
    be assigned to ``character``. Instead, a item will only be available if
    that item belongs to ``character``'s campaign.

    >>> from gurps_manager import factories
    >>> from django.forms.models import ModelForm
    >>> character = factories.CharacterFactory.create()
    >>> formset_cls = possession_form(character)
    >>> formset_cls.__name__
    'PossessionForm'
    >>> ModelForm in formset_cls.__bases__
    True

    """
    class PossessionForm(ModelForm):
        """A form for creating or editing a ``Possession`` object."""
        item = ModelChoiceField(
            queryset=models.Spell.objects.filter( # pylint: disable=E1101
                campaign=character.campaign
            )
        )

        class Meta(object):
            """Form attributes that are not custom fields."""
            model = models.Possession

    return PossessionForm

def possession_formset(character):
    """Generate an inline formset class for ``Possession`` objects.

    The inline formset class can be used to edit ``Possession`` objects
    belonging to a particular ``Character`` object.

    """
    return inlineformset_factory(
        models.Character,
        models.Possession,
        extra=5,
        form=character_skill_form(character)
    )

def trait_formset():
    """Generate an inline formset class for ``Trait`` objects.

    The inline formset can be used to edit ``Trait`` objects belonging to a
    particular ``Character`` object.

    """
    return inlineformset_factory(
        models.Character,
        models.Trait,
        extra=5
    )

def hit_location_formset():
    """Generate an inline formset class for ``HitLocation`` objects.

    The inline formset can be used to edit ``HitLocation`` objects belonging to
    a particular ``Character`` object.

    """
    return inlineformset_factory(
        models.Character,
        models.HitLocation,
        extra=5
    )

def campaign_spells_formset():
    """Generate an inline formset class for ``Spell`` objects.

    The inline formset can be used to edit ``Spell`` objects belonging to
    a particular ``Campaign`` object.

    """
    return inlineformset_factory(
        models.Campaign,
        models.Spell,
        extra=5
    )

def campaign_items_formset():
    """Generate an inline formset class for ``Item`` objects.

    The inline formset can be used to edit ``Item`` objects belonging to
    a particular ``Campaign`` object.

    """
    return inlineformset_factory(
        models.Campaign,
        models.Item,
        extra=5
    )
