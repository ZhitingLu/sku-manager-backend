"""
Test custom django management commands
"""

from unittest.mock import patch

from psycopg import OperationalError as PsycopgError

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands"""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready"""
        patched_check.return_value = True  # Mocking the behavior of `check`
        
        # Call the command to check the database status
        call_command('wait_for_db')
        
        # Assert that `check` was called once with the expected arguments
        patched_check.assert_called_once_with(databases=['default'])
     
    @patch('time.sleep')   
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError"""
        # create a list with two instances of PsycopgError."
        # So the first two times the mocked check() method is called, it will raise a PsycopgError.
        patched_check.side_effect = [PsycopgError] * 2 + \
            [OperationalError] * 3 + [True]
            # create a list with three instances of OperationalError." 
            # So the next three times the mocked check() method is called, it will raise an OperationalError
            # So after raising OperationalError three times, 
            # the next call will return True (indicating that the database is ready).
            
        call_command("wait_for_db")
        
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])