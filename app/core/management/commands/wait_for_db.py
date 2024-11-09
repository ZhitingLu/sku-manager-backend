"""
Django command to wait for the database to be available
"""
import time

from psycopg import OperationalError as PyscopgOpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Django command to wait for databse
    """

    def handle(self, *args, **options):
        """Entrypoint for command"""
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                # checks the database connection for the default database
                self.check(databases=['default'])
                db_up = True
            except (PyscopgOpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second ...')
                # pause for 1 second before attempting to connect again.
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
