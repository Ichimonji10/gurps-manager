"""django-tables2 class definitions.

django-tables2 can be used to generate HTML tables from models. Those tables can
then be displayed in templates. See:
https://github.com/bradleyayers/django-tables2

"""
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from gurps_manager import models
import django_tables2 as tables

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

class CampaignTable(tables.Table):
    """An HTML table displaying ``Campaign`` objects."""
    actions = tables.Column(empty_values=(), orderable=False)

    class Meta(object):
        """Table attributes that are not custom fields."""
        model = models.Campaign

    def render_description(self, value):
        """Define how the ``description`` column should be rendered.

        ``value`` represents a single cell of data from the table.

        """
        return _truncate_string(value)

    def render_actions(self, record):
        """Define how the ``actions`` column should be rendered.

        ``record`` represents a row of data from the database (and,
        consequently, a row in the table).

        """
        return mark_safe(_restful_links('campaign', record.id))

class CharacterTable(tables.Table):
    """An HTML table displaying ``Campaign`` objects."""
    spent_points = tables.Column(empty_values=())
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

        """
        return _truncate_string(value)

    def render_actions(self, record):
        """Define how the ``actions`` column should be rendered.

        ``record`` represents a row of data from the database (and,
        consequently, a row in the table).

        """
        return mark_safe(_restful_links('character', record.id))

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
