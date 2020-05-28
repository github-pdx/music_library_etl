"""Unit tests to insert JSON media tags into PostgreSQL."""
import unittest
import os
import pathlib
from media_etl.db.postgres_api import PostgresMedia

BASE_DIR, SCRIPT_NAME = os.path.split(os.path.abspath(__file__))
PARENT_PATH, CURR_DIR = os.path.split(BASE_DIR)


class TestDatabase(unittest.TestCase):
    """Test case class for postgres_api.py."""

    def setUp(self):
        self.pg_api = PostgresMedia(hostname='localhost',
                                    port_num=5432,
                                    username='run_admin_run',
                                    password='run_pass_run')
        self.db_user = 'new_user'
        self.db_pass = 'run_pass_run'
        self.db_name = 'new_media_db'
        self.valid_json_path = pathlib.Path(PARENT_PATH, 'data', 'input')
        self.valid_json_file = pathlib.Path(PARENT_PATH, 'data',
                                            'input', 'media_lib.json')
        self.invalid_json_path = pathlib.Path(PARENT_PATH, 'does', 'not_exist')

    def test_is_connected(self):
        """Verifies media_db connection status with valid input."""
        if self.pg_api.conn_status:
            self.assertTrue(self.pg_api.is_connected())
        else:
            self.assertFalse(self.pg_api.is_connected())

    def test_show_database_status(self):
        """Displays postgres status for media_db instance."""
        if self.pg_api.conn_status:
            self.assertIsNone(self.pg_api.show_database_status())

    def test_query_with_parmas(self):
        """Checks query execution with result set with params."""
        param_query = ("SELECT * FROM artist "
                       "WHERE artist_name = (%s)")
        p_result_set = self.pg_api.query(query=param_query, params=['Ravel'])
        self.assertIsNotNone(p_result_set)

    def test_query_without_parmas(self):
        """Checks query execution with result set without params."""
        no_parma_query = "SELECT * FROM artist"
        np_result_set = self.pg_api.query(query=no_parma_query)
        self.assertIsNotNone(np_result_set)

    def test_query_empty(self):
        """Checks query execution on invalid table."""
        param_query = "SELECT * FROM unknown_table"
        p_result_set = self.pg_api.query(query=param_query)
        self.assertFalse(len(p_result_set) > 0)

    def test_query_malformed(self):
        """Checks query execution on malformed query."""
        param_query = "MALFORMED * FRUM tableau"
        p_result_set = self.pg_api.query(query=param_query)
        self.assertFalse(len(p_result_set) > 0)
        param_query = ("SELECT * FROM artist "
                       "WHERE artist_name = (-%d)")
        p_result_set = self.pg_api.query(query=param_query, params=['Ravel'])
        self.assertFalse(len(p_result_set) > 0)

    def test_create_role(self):
        """Verifies role creation for media_db postgres instance."""
        status = self.pg_api.create_role(username='new_user',
                                         password='run_pass_run')
        self.assertTrue('SUCCESS' in status)

    def test_recreate_database(self):
        """Recreates new media_db postgres initialization."""
        status = self.pg_api.recreate_database(db_name='new_media_db',
                                               owner='new_user')
        self.assertTrue('SUCCESS' in status)

    def test_create_tables(self):
        """Recreate all postgres database tables."""
        status = self.pg_api.create_tables()
        self.assertTrue('SUCCESS' in status)

    def test_process_file(self):
        """Extract/Transform media_lib.json, Load into postgres media_db."""
        status = self.pg_api.process_file(self.valid_json_file)
        self.assertTrue(status)

    def test_process_data(self):
        """Find all .json input files."""
        status = self.pg_api.create_tables()
        status = self.pg_api.process_data(self.valid_json_path)
        self.assertTrue(status)
        status = self.pg_api.process_data(self.invalid_json_path)
        self.assertFalse(status)

    def test_drop_tables(self):
        """Drop all tables in postgres for media_db."""
        status = self.pg_api.drop_tables()
        self.assertTrue('SUCCESS' in status)

    def test_close(self):
        """Verify close postgres connection."""
        self.pg_api.close()
        self.assertTrue(self.pg_api.is_connected())

    def tearDown(self):
        self.pg_api.close()


if __name__ == '__main__':
    unittest.main()
