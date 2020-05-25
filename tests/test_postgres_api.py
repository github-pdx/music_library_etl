import unittest
import os
import pathlib
import random
from media_etl.db.postgres_api import PostgresMedia

BASE_DIR, SCRIPT_NAME = os.path.split(os.path.abspath(__file__))
PARENT_PATH, CURR_DIR = os.path.split(BASE_DIR)


class TestDatabase(unittest.TestCase):
    """Test case class for postgres_api.py"""

    def setUp(self):
        self.pgdb_api = PostgresMedia(hostname='localhost',
                                      port_num=5432,
                                      username='run_admin_run',
                                      password='run_pass_run')

    def test_is_connected(self):
        if self.pgdb_api.conn_status:
            self.assertTrue(self.pgdb_api.is_connected())
        else:
            self.assertFalse(self.pgdb_api.is_connected())

    def test_show_database_status(self):
        if self.pgdb_api.conn_status:
            self.assertIsNone(self.pgdb_api.show_database_status())

    def test_query(self):
        self.assertTrue(True)

    def test_create_role(self):
        self.assertTrue(True)

    def test_recreate_database(self):
        self.assertTrue(True)

    def test_drop_tables(self):
        self.assertTrue(True)

    def test_create_tables(self):
        self.assertTrue(True)

    def test_process_file(self):
        self.assertTrue(True)

    def test_process_data(self):
        self.assertTrue(True)

    def test_close(self):
        self.assertTrue(True)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
