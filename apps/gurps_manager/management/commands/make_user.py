"""Create a command named ``make_user``."""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
# optparse is deprecated in the version of python we're using
# however, Django has not moved to argparse for commands yet
# this is because the minimum version of python that Django requires
# is prior to the addition of argparse
# TODO: wait until Django updates to argparse
from optparse import make_option

class Command(BaseCommand):
    """Defines how to register the ``make_user`` command with ``manage.py``."""
    args = '<username><password>'
    help = 'Create a user object for the application.'

    option_list = BaseCommand.option_list + (
        make_option('--admin',
            action='store_true',
            dest='admin',
            default=False,
            help='make the user an admin'),
        )

    def handle(self, *args, **options):
        """Create a User with the given username and password"""
        # Grab the username and password out of the args list
        username = args[0]
        password = args[1]
        email = ''
        # Create the user object
        user = User.objects.create_user(username, email, password)

        # Make the user an admin if the flag is set
        if options['admin']:
            user.is_staff = True
            user.is_superuser = True
            user.save()
