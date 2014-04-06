"""django-tables2 class definitions.

django-tables2 can be used to generate HTML tables from models. Those tables can
then be displayed in templates. See:
https://github.com/bradleyayers/django-tables2

"""
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from gurps_manager import models
import django_tables2 as tables

# FIXME: Add doctests for the various render_* methods in this module. See
# `CampaignTable.render_description` for inspiration.

# pylint: disable=R0903
# "Too few public methods (0/2)"
# It is both common and OK for a table class to have no methods.
#
# pylint: disable=W0232
# "Class has no __init__ method"
# It is both common and OK for a table class to have no __init__ method.
#
# pylint: disable=R0201
# Framework requires use of methods rather than functions
def campaign_table(user):
    """Generate a table class for ``Campaign`` objects.

    ``user`` is a ``User`` model object.

    The table class returned is suitable for displaying characters

    >>> from django.core.urlresolvers import reverse
    >>> from django.utils.safestring import mark_safe
    >>> from gurps_manager import models
    >>> import django_tables2 as tables
    >>> from gurps_manager import factories
    >>> user = factories.UserFactory.create()
    >>> table_cls = campaign_table(user)
    >>> table_cls.__name__
    'CampaignTable'
    >>> tables.Table in table_cls.__bases__
    True

    """
    class CampaignTable(tables.Table):
        """An HTML table displaying ``Campaign`` objects."""
        actions = tables.Column(empty_values=(), orderable=False)

        class Meta(object):
            """Table attributes that are not custom fields."""
            model = models.Campaign
            exclude = ('id',)
            sequence = ('name', 'description', 'owner', '...')

        def render_description(self, value):
            """Define how the ``description`` column should be rendered.

            ``value`` represents a single cell of data from the table.

            >>> from gurps_manager.models import Campaign
            >>> from gurps_manager.tables import _truncate_string
            >>> table = CampaignTable(Campaign.objects.all())
            >>> string = 'a' * 130
            >>> table.render_description(string) == _truncate_string(string)
            True
            >>> string = 'a' * 150
            >>> table.render_description(string) == _truncate_string(string)
            True

            """
            return _truncate_string(value)

        def render_actions(self, record):
            """Define how the ``actions`` column should be rendered.

            ``record`` represents a row of data from the database (and,
            consequently, a row in the table).

            """
            if record.owner == user:
                return mark_safe(_restful_links('campaign', record.id))
            else:
                return mark_safe('<a href="{}">View</a>'.format(
                    _read_url('campaign', record.id)
                ))

    return CampaignTable

def character_table(user):
    """Generate a table class for ``Character`` objects.

    ``user`` is a ``User`` model object.

    The table class returned is suitable for displaying characters

    >>> from django.core.urlresolvers import reverse
    >>> from django.utils.safestring import mark_safe
    >>> from gurps_manager import models
    >>> import django_tables2 as tables
    >>> from gurps_manager import factories
    >>> user = factories.UserFactory.create()
    >>> table_cls = character_table(user)
    >>> table_cls.__name__
    'CharacterTable'
    >>> tables.Table in table_cls.__bases__
    True

    """
    class CharacterTable(tables.Table):
        """An HTML table displaying ``Character`` objects."""
        spent_points = tables.Column(empty_values=(), orderable=False)
        actions = tables.Column(empty_values=(), orderable=False)

        class Meta(object):
            """Table attributes that are not custom fields."""
            model = models.Character
            fields = ('name', 'description', 'total_points')

        def render_spent_points(self, record):
            """Define how the ``spent_points`` column should be rendered.

            ``record`` represents a row of data from this table.

            """
            return record.total_points_spent()

        def render_description(self, value):
            """Define how the ``description`` column should be rendered.

            ``value`` represents a single cell of data from the table.

            >>> from gurps_manager.models import Character
            >>> table = CharacterTable(Character.objects.all())
            >>> string = 'a' * 130
            >>> table.render_description(string) == _truncate_string(string)
            True
            >>> string = 'a' * 150
            >>> table.render_description(string) == _truncate_string(string)
            True

            """
            return _truncate_string(value)

        def render_actions(self, record):
            """Define how the ``actions`` column should be rendered.

            ``record`` represents a row of data from the database (and,
            consequently, a row in the table).

            """
            if record.owner == user:
                return mark_safe(_restful_links('character', record.id))
            else:
                return mark_safe('<a href="{}">View</a>'.format(
                    _read_url('character', record.id)
                ))

    return CharacterTable

class CharacterSkillTable(tables.Table):
    """An HTML table displaying ``CharacterSkill`` objects."""
    score = tables.Column(empty_values=(), orderable=False)
    category = tables.Column(empty_values=(), orderable=False)
    difficulty = tables.Column(empty_values=(), orderable=False)

    class Meta(object):
        """Table attributes that are not custom fields."""
        model = models.CharacterSkill
        exclude = ('character', 'id')
        sequence = ('skill', '...')

    def render_difficulty(self, record):
        """Define how the ``difficulty`` column should be rendered.

        ``record`` represents a row of data from this table

        """
        return record.skill.get_difficulty_display

    def render_category(self, record):
        """Define how the ``category`` column should be rendered.

        ``record`` represents a row of data from this table

        """
        return record.skill.get_category_display

    def render_score(self, record):
        """Define how the ``score`` column should be rendered.

        ``record`` represents a row of data from this table

        """
        return record.score()

class CharacterSpellTable(tables.Table):
    """An HTML table displaying ``CharacterSpell`` objects."""
    score = tables.Column(empty_values=(), orderable=False)
    school = tables.Column(empty_values=(), orderable=False)
    resist = tables.Column(empty_values=(), orderable=False)
    duration = tables.Column(empty_values=(), orderable=False)
    cast_time = tables.Column(empty_values=(), orderable=False)
    initial_fatigue_cost = tables.Column(empty_values=(), orderable=False)
    maintenance_fatigue_cost = tables.Column(empty_values=(), orderable=False)
    difficulty = tables.Column(empty_values=(), orderable=False)

    class Meta(object):
        """Table attributes that are not custom fields."""
        model = models.CharacterSpell
        exclude = ('character', 'id')
        sequence = ('spell', '...')

    def render_score(self, record):
        """Define how the ``score`` column should be rendered.

        ``record`` represents a row of data from this table

        """
        return record.score()

    def render_school(self, record):
        """Define how the ``school`` column should be rendered.

        ``record`` represents a row of data from this table

        """
        return record.spell.school

    def render_resist(self, record):
        """Define how the ``resist`` column should be rendered.

        ``record`` represents a row of data from this table

        """
        return record.spell.resist

    def render_duration(self, record):
        """Define how the ``duration`` column should be rendered.

        ``record`` represents a row of data from this table

        """
        return record.spell.duration

    def render_cast_time(self, record):
        """Define how the ``cast time`` column should be rendered.

        ``record`` represents a row of data from this table

        """
        return str(record.spell.cast_time) + ' seconds'

    def render_initial_fatigue_cost(self, record):
        """Define how the ``initial fatigue cost`` column should be rendered.

        ``record`` represents a row of data from this table

        """
        return record.spell.initial_fatigue_cost

    def render_maintenance_fatigue_cost(self, record):
        # pylint: disable=C0301
        """Define how the ``maintenance fatigue cost`` column should be rendered.

        ``record`` represents a row of data from this table

        """
        return record.spell.maintenance_fatigue_cost

    def render_difficulty(self, record):
        """Define how the ``difficulty`` column should be rendered.

        ``record`` represents a row of data from this table

        """
        return record.spell.get_difficulty_display


class PossessionTable(tables.Table):
    """An HTML table displaying ``Possession`` objects."""
    value = tables.Column(empty_values=(), orderable=False)
    total_value = tables.Column(empty_values=(), orderable=False)
    weight = tables.Column(empty_values=(), orderable=False)
    total_weight = tables.Column(empty_values=(), orderable=False)
    description = tables.Column(empty_values=(), orderable=False)

    class Meta(object):
        """Table attributes that are not custom fields."""
        model = models.Possession
        exclude = ('character', 'id')
        sequence = ('item', '...')

    def render_description(self, record):
        """Define how the ``description`` column should be rendered.

        ``record`` represents a row of data from this table

        """
        return _truncate_string(record.item.description)

    def render_value(self, record):
        """Define how the ``value`` column should be rendered.

        ``record`` represents a row of data from this table

        """
        return '{:.2f}'.format(record.item.value)

    def render_total_value(self, record):
        """Define how the ``total value`` column should be rendered.

        ``record`` represents a row of data from this table

        """
        return '{:.2f}'.format(record.item.value * record.quantity)

    def render_weight(self, record):
        """Define how the ``weight`` column should be rendered.

        ``record`` represents a row of data from this table

        """
        return '{:.2f} lbs.'.format(record.item.weight)

    def render_total_weight(self, record):
        """Define how the ``total weight`` column should be rendered.

        ``record`` represents a row of data from this table

        """
        return '{:.2f} lbs.'.format(record.item.weight * record.quantity)

class TraitTable(tables.Table):
    """An HTML table displaying ``Trait`` objects."""

    class Meta(object):
        """Table attributes that are not custom fields."""
        model = models.Trait
        exclude = ('character', 'id')
        sequence = ('name', 'description', '...')

class HitLocationTable(tables.Table):
    """An HTML table displaying ``HitLocation`` objects."""

    class Meta(object):
        """Table attributes that are not custom fields."""
        model = models.HitLocation
        exclude = ('character', 'id')
        sequence = ('name', '...')

class ItemTable(tables.Table):
    """An HTML table displaying ``Item`` objects."""

    class Meta(object):
        """Table attributes that are not custom fields."""
        model = models.Item
        exclude = ('campaign', 'id',)

class SpellTable(tables.Table):
    """An HTML table displaying ``Spell`` objects."""

    class Meta(object):
        """Table attributes that are not custom fields."""
        model = models.Spell
        sequence = ('name', 'difficulty', '...',)
        exclude = ('campaign', 'id',)

    def render_difficulty(self, record):
        """Define how the ``difficulty`` column should be rendered.

        ``record`` represents a row of data from this table

        """
        return record.get_difficulty_display

# private methods --------------------------------------------------------------

def _read_url(resource, resource_id):
    """Generate the path for reading ``resource`` number ``resource_id``.

    >>> import re
    >>> None != re.search(r'/campaign/1234/$', _read_url('campaign', 1234))
    True

    """
    return reverse(
        'gurps-manager-{}-id'.format(resource),
        args=[resource_id]
    )

def _update_url(resource, resource_id):
    """Generate the path for updating ``resource`` number ``resource_id``.

    >>> import re
    >>> None != re.search(
    ...     r'/campaign/1234/update-form/$',
    ...     _update_url('campaign', 1234)
    ... )
    True

    """
    return reverse(
        'gurps-manager-{}-id-update-form'.format(resource),
        args=[resource_id]
    )

def _delete_url(resource, resource_id):
    """Generate the path for deleting ``resource`` number ``resource_id``.

    >>> import re
    >>> None != re.search(
    ...     r'/campaign/1234/delete-form/$',
    ...     _delete_url('campaign', 1234)
    ... )
    True

    """
    return reverse(
        'gurps-manager-{}-id-delete-form'.format(resource),
        args=[resource_id]
    )

def _restful_links(resource, resource_id):
    """Generate links for reading, updating and deleting ``resource`` number
    ``resource_id``.

    """
    return \
        '<a href="{}">View</a> - ' \
        '<a href="{}">Edit</a> - ' \
        '<a href="{}">Delete</a>'.format(
            _read_url(resource, resource_id),
            _update_url(resource, resource_id),
            _delete_url(resource, resource_id),
        )

def _truncate_string(string):
    """If ``string`` is too long, truncate it and append an ellipsis.

    ``string`` itself is not affected. A new string is returned.

    >>> target_length = 140
    >>> string = 'x' * target_length
    >>> _truncate_string(string) == string
    True
    >>> truncated_string = _truncate_string(string + 'x')
    >>> truncated_string != string
    True
    >>> truncated_string[-1] == chr(8230)
    True
    >>> len(truncated_string) == target_length
    True

    """
    limit = 140
    if len(string) > limit:
        return string[:limit - 1] + chr(8230)
    else:
        return string
