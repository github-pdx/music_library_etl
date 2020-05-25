# -*- coding: UTF-8 -*-
"""Media driver module to insert JSON dumps into PostgreSQL."""
import os
import sys
import pathlib
import inspect
import traceback
import psycopg2
import pandas
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import media_etl.db.spotify as spotify
import media_etl.db.postgres_insert_queries as sql

BASE_DIR, SCRIPT_NAME = os.path.split(os.path.abspath(__file__))
PARENT_PATH, CURR_DIR = os.path.split(BASE_DIR)
TWO_PARENT_PATH = os.sep.join(pathlib.Path(BASE_DIR).parts[:-2])
PRIVATE_CONFIG = False


class PostgresMedia:
    """Class to add/remove media tags to Postgres backend."""

    @classmethod
    def __init__(cls, hostname: str = 'localhost',
                 port_num: int = 5432,
                 db_name: str = 'media_db',
                 username: str = 'run_admin_run',
                 password: str = 'run_pass_run'):
        try:
            cls.__is_connected = False
            cls.__hostname = hostname
            cls.__port_num = port_num
            cls.__db_name = db_name
            cls.__username = username
            cls.__password = password
            cls.db_conn = psycopg2.connect(f"host={hostname} "
                                           f"port={port_num} "
                                           f"dbname={db_name} "
                                           f"user={username} "
                                           f"password={password}",
                                           connect_timeout=1)
            cls.db_conn.set_session(autocommit=True)
            cls.db_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cls.conn_status = cls.is_connected()
            cls.db_cur = cls.db_conn.cursor()
            if PRIVATE_CONFIG:
                config_path = pathlib.Path(TWO_PARENT_PATH, 'private_cfg',
                                           'spotify.cfg')
            else:
                config_path = pathlib.Path(TWO_PARENT_PATH, 'spotify.cfg')
            cls.spotify = spotify.SpotifyClient(config_path)
        except (OSError, psycopg2.OperationalError):
            cls.db_conn = None
            cls.__show_exception()
            print(f"hostname: {cls.__hostname}\n"
                  f"port: {cls.__port_num}\n"
                  f"db_name: {cls.__db_name}\n"
                  f"username: {cls.__username}\n"
                  f"password: {cls.__password}")

    @classmethod
    def is_connected(cls) -> bool:
        """Checks for valid connection (either postgres or media_db)."""
        try:
            if cls.db_conn:
                return True
        except psycopg2.OperationalError as exc:
            print("ERROR: not connected", exc)
        return False

    @classmethod
    def get_connection(cls):
        """Return client connection to 'media_db' database."""
        return cls.db_conn

    @staticmethod
    def __show_exception():
        """Custom traceback exception wrapper."""
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                  limit=2, file=sys.stdout)

    @classmethod
    def show_database_status(cls) -> None:
        """Displays current list of Postgres databases on host."""
        def_name = inspect.currentframe().f_code.co_name
        if cls.is_connected():
            pg_ver = str(cls.db_conn.server_version)
            dot_ver = f"{pg_ver[0:1]}.{pg_ver[1:3]}.{pg_ver[-2:]}"
            print(f"{def_name}()\n   postgres version: {dot_ver}")
            cls.db_cur.execute("select relname from pg_class "
                               "where relkind='r' and "
                               "relname !~ '^(pg_|sql_)';")
            print(f"   tables: {cls.db_cur.fetchall()}")

    @classmethod
    def query(cls, query: str, params: list = []):
        """Query media database for result set based on params."""
        try:
            pq_query = f"{query} VALUES {params};"
            print(f"\n{pq_query}")
            cls.db_cur.execute(query, params)
            for result in cls.db_cur.fetchall():
                print(result)
        except (SyntaxError, TypeError):
            cls.__show_exception()

    @classmethod
    def create_role(cls, username: str, password: str):
        """Create new admin role to access media database."""
        def_name = inspect.currentframe().f_code.co_name
        # run_pass_run = 'md5239b17d24927a16de2aba75c9bde23e2'
        try:
            check_user_query = (f"SELECT rolname FROM pg_roles "
                                f"WHERE rolname IN ('{username}');")
            cls.db_cur.execute(check_user_query)
            db_user = cls.db_cur.fetchone()
            if not db_user:
                cls.db_cur.execute(f"CREATE ROLE {username} WITH "
                                   f"LOGIN PASSWORD '{password}' "
                                   f"SUPERUSER CREATEDB CREATEROLE NOINHERIT "
                                   f"LOGIN CONNECTION LIMIT -1 "
                                   f"VALID UNTIL '2020-12-31';")
            status = f"SUCCESS! {def_name}: {username}"
        except (OSError, psycopg2.OperationalError,
                psycopg2.errors.InFailedSqlTransaction) as exc:
            status = f"~!ERROR!~ {def_name}() {sys.exc_info()[0]} {exc}"
        print(status)

    @classmethod
    def recreate_database(cls, db_name: str, owner: str):
        """Create media Postgres database."""
        def_name = inspect.currentframe().f_code.co_name
        try:
            cls.db_cur.execute(f"DROP DATABASE IF EXISTS {db_name};")
            cls.db_cur.execute(f"CREATE DATABASE {db_name} "
                               f"WITH ENCODING = 'UTF8' "
                               f"OWNER = {owner} "
                               f"CONNECTION LIMIT = -1;")
            status = f"SUCCESS! {def_name}: {db_name}"
        except (OSError, psycopg2.OperationalError,
                psycopg2.errors.InFailedSqlTransaction,
                psycopg2.errors.ActiveSqlTransaction) as exc:
            status = f"~!ERROR!~ {def_name}() {sys.exc_info()[0]}\n{exc}"
        print(status)

    @classmethod
    def drop_tables(cls):
        """Remove tables from Postgres media database."""
        def_name = inspect.currentframe().f_code.co_name
        try:
            print(f"{def_name}() {len(sql.TABLES)} tables:")
            for table in sql.TABLES:
                query = f"DROP TABLE IF EXISTS {table}"
                print(f"   {query}")
                cls.db_cur.execute(query)
        except (OSError, psycopg2.OperationalError):
            cls.__show_exception()

    @classmethod
    def create_tables(cls):
        """Create tables into Postgres database."""
        def_name = inspect.currentframe().f_code.co_name
        try:
            print(f"{def_name}() {len(sql.TABLES)} tables:")
            for query in sql.CREATE_TABLES_QUERIES:
                print(f"   {query}")
                cls.db_cur.execute(query)
        except (OSError, psycopg2.OperationalError):
            cls.__show_exception()

    @classmethod
    def process_file(cls, input_path: pathlib.Path):
        """Driver to parse JSON file and commit to Postgres database."""
        try:
            df = pandas.read_json(input_path, lines=False,
                                  encoding='utf-8',
                                  orient='split')
            for column, series in df.iterrows():
                if cls.spotify.run_spotify():
                    artist_name = series['artist']
                    series['artist_id'] = cls.spotify.get_artist_id(
                        artist_name)
                for table, headers in sql.HEADERS.items():
                    data = series[headers]
                    cls.db_cur.execute(sql.INSERTS[table], data)
        except (IndexError, KeyError, psycopg2.OperationalError):
            cls.__show_exception()

    @classmethod
    def process_data(cls, input_path: pathlib.Path):
        """Finds source JSON files recursively from input path."""
        file_path_list = [p.absolute() for p in
                          sorted(input_path.rglob("*.json"))
                          if p.is_file()]
        print(f"{len(file_path_list)} files found in "
              f"'{os.sep.join(input_path.parts[-3:])}'")
        for idx, json_path in enumerate(file_path_list, 0):
            cls.process_file(json_path)
            print(f"  processing: file_{idx:02d}: {json_path.name}")

    @classmethod
    def close(cls):
        cls.db_cur.close()
        cls.db_conn.close()