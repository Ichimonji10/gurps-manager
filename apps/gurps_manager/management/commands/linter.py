"""This Module allows the automatic linting
of the entire application with pylint
"""
from django.core.management.base import BaseCommand, CommandError
from pylint.lint import Run
import os

class Command(BaseCommand):
    """Allows this file to be called as a command on manage.py"""
    help = 'Calls Pylint on all the .py files in the application'

    def handle(self, *args, **options):
        """This does the work when this is called by manage.py"""
        python_files = []

        for root, dirs, files in os.walk(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            '../../..'
            )):
            for file in files:
                if file.endswith(".py"):
                    python_files.append(
                        os.path.relpath(os.path.join(root, file))
                        )

        print('Beginning linting...')

        Run(python_files)

        print('Linting finished!')
