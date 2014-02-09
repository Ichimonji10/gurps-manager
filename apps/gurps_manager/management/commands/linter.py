"""Create a command named ``linter``."""
from django.core.management.base import BaseCommand
from pylint.lint import Run
import os

class Command(BaseCommand):
    """Defines how to register the ``linter`` command with ``manage.py``."""
    help = 'Lint all .py files in this application, using Pylint.'

    def handle(self, *args, **options):
        """Search for .py files and lint them."""
        python_files = []
        for root, dirs, files in os.walk(os.path.join( # pylint: disable=W0612
            os.path.dirname(os.path.realpath(__file__)),
            '..',
            '..',
            '..'
        )):
            for file in files:
                if file.endswith(".py"):
                    python_files.append(
                        os.path.relpath(os.path.join(root, file))
                    )
        Run(python_files)
