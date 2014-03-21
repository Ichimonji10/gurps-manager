"""Create a command named ``make_user``."""
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Defines how to register the ``make_user`` command with ``manage.py``."""
    args = '<username><password>'
    help = 'Create a user object for the application.'

    def handle(self, *args, **options):
        """Create a User with the given username and password"""
