"""Create a command named ``make_user``."""
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
# optparse is deprecated in the version of python we're using. However, Django
# has not moved to argparse for commands yet. This is because the minimum
# version of python that Django requires is prior to the addition of argparse
# TODO: wait until Django updates to argparse
from optparse import make_option

class Command(BaseCommand):
    """Defines how to register the ``make_user`` command with ``manage.py``."""
    args = '<username> <password>'
    help = 'Create a user object for the application.'
    option_list = BaseCommand.option_list + (
        make_option(
            '--admin',
            action='store_true',
            dest='admin',
            default=False,
            help='make the user an admin'
        ),
    )

    def handle(self, *args, **options):
        """Create a User object."""
        username = args[0]
        password = args[1]
        email = ''

        user = User.objects.create_user(username, email, password)
        if options['admin']:
            user.is_staff = True
            user.is_superuser = True
            user.save()
