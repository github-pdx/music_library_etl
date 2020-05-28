# -*- coding: UTF-8 -*-
"""Media driver module to insert JSON media tags into PostgreSQL."""
import os
import sys
import pathlib
import inspect
import traceback
import psycopg2
import pandas
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from db.spotify import SpotifyClient
from db import postgres_insert_queries as sql

BASE_DIR, SCRIPT_NAME = os.path.split(os.path.abspath(__file__))
PARENT_PATH, CURR_DIR = os.path.split(BASE_DIR)
TWO_PARENT_PATH = os.sep.join(pathlib.Path(BASE_DIR).parts[:-2])


class PostgresMedia:
    """Class to add/remove media tags to Postgres backend."""

    @classmethod
    def __init__(cls, hostname: str = 'localhost',
                 port_num: int = 5432,
                 db_name: str = 'media_db',
                 username: str = 'run_admin_run',
                 password: str = 'run_pass_run',
                 private_cfg=False):
        try:
            cls.__is_connected = False
            cls.__hostname = hostname
            cls.__port_num = port_num
            cls.__db_name = db_name
            cls.__username = username
            cls.__password = password
            cls.__private_cfg = private_cfg
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
            if cls.__private_cfg:
                config_path = pathlib.Path(TWO_PARENT_PATH, 'private_cfg',
                                           'spotify.cfg')
            else:
                config_path = pathlib.Path(TWO_PARENT_PATH, 'spotify.cfg')
            cls.spotify = SpotifyClient(config_path)
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
    def show_database_status(cls) -> list:
        """Displays current list of Postgres databases on host."""
        def_name = inspect.currentframe().f_code.co_name
        if cls.is_connected():
            pg_ver = str(cls.db_conn.server_version)
            dot_ver = f"{pg_ver[0:1]}.{pg_ver[1:3]}.{pg_ver[-2:]}"
            print(f"{def_name}()\n   postgres version: {dot_ver}"
                  f"\n   database: {cls.__db_name}")
            cls.get_tables()

    @classmethod
    def get_tables(cls) -> list:
        """Display current list of media_lib tables."""
        cls.db_cur.execute("select relname from pg_class "
                           "where relkind='r' and "
                           "relname !~ '^(pg_|sql_)';")
        result_set = cls.db_cur.fetchall()
        print(f"   tables: {result_set}")
        return result_set

    @classmethod
    def query(cls, query: str, params: list = []) -> list:
        """Query media database for result set based on params."""
        result_set = []
        try:
            if isinstance(query, str) and query:
                if isinstance(params, list) or params:
                    if len(params) == 0:
                        pq_query = f"{query};"
                    else:
                        pq_query = f"{query} VALUES {params};"
                    print(f"\n{pq_query}")
                    cls.db_cur.execute(query, params)
                    result_set = cls.db_cur.fetchall()
                    for result in result_set:
                        print(result)
        except (TypeError, ValueError, psycopg2.errors.UndefinedTable,
                psycopg2.errors.SyntaxError):
            cls.__show_exception()
        return result_set

    @classmethod
    def create_role(cls, username: str, password: str) -> str:
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
                                   f"CREATEDB CREATEROLE NOINHERIT "
                                   f"CONNECTION LIMIT -1 "
                                   f"VALID UNTIL '2022-12-31';")
            status = f"SUCCESS! {def_name}: {username}"
        except (OSError, psycopg2.OperationalError,
                psycopg2.errors.InFailedSqlTransaction) as exc:
            status = f"~!ERROR!~ {def_name}() {sys.exc_info()[0]} {exc}"
        print(status)
        return status

    @classmethod
    def recreate_database(cls, db_name: str, owner: str) -> str:
        """Create media Postgres database."""
        def_name = inspect.currentframe().f_code.co_name
        if isinstance(db_name, str) and db_name:
            if isinstance(owner, str) and owner:
                try:
                    cls.db_cur.execute(f"DROP DATABASE IF EXISTS {db_name};")
                    cls.db_cur.execute(f"CREATE DATABASE {db_name} "
                                       f"WITH ENCODING = 'UTF8' "
                                       f"OWNER = {owner} "
                                       f"CONNECTION LIMIT = -1;")
                    status = f"SUCCESS! {def_name}() {db_name}"
                except (OSError, psycopg2.OperationalError,
                        psycopg2.errors.UndefinedObject,
                        psycopg2.errors.InFailedSqlTransaction,
                        psycopg2.errors.ActiveSqlTransaction) as e:
                    status = f"~!ERROR!~ {def_name}() {sys.exc_info()[0]}\n{e}"
                print(status)
                return status

    @classmethod
    def drop_tables(cls) -> str:
        """Remove tables from Postgres media database."""
        def_name = inspect.currentframe().f_code.co_name
        try:
            print(f"{def_name}() {len(sql.TABLES)} tables:")
            for table in sql.TABLES:
                query = f"DROP TABLE IF EXISTS {table}"
                print(f"   {query}")
                cls.db_cur.execute(query)
            status = f"SUCCESS! {def_name}()"
        except (OSError, psycopg2.OperationalError) as e:
            status = f"~!ERROR!~ {def_name}() {sys.exc_info()[0]}\n{e}"
        return status

    @classmethod
    def create_tables(cls) -> str:
        """Create tables into Postgres database."""
        def_name = inspect.currentframe().f_code.co_name
        try:
            print(f"{def_name}() {len(sql.TABLES)} tables:")
            for query in sql.CREATE_TABLES_QUERIES:
                print(f"   {query}")
                cls.db_cur.execute(query)
            status = f"SUCCESS! {def_name}()"
        except (OSError, psycopg2.OperationalError):
            cls.__show_exception()
            status = f"~!ERROR!~ {def_name}() {sys.exc_info()[0]}\n{e}"
        return status

    @classmethod
    def process_file(cls, input_path: pathlib.Path) -> bool:
        """Driver to parse JSON file and commit to Postgres database."""
        query_status = []
        inserts_ok = False
        if isinstance(input_path, pathlib.Path) and input_path:
            try:
                df = pandas.read_json(input_path, lines=False,
                                      encoding='utf-8',
                                      orient='split')
                for column, series in df.iterrows():
                    series['artist_id'] = cls.spotify.get_artist_id(
                        series['artist_name'])
                    series['album_id'] = cls.spotify.get_album_id(
                        series['artist_id'], series['album_title'])
                    for table, headers in sql.HEADERS.items():
                        data = series[headers]
                        cls.db_cur.execute(sql.INSERTS[table], data)
                        # returns 1 if query was successful
                        query_status.append(cls.db_cur.rowcount)
                inserts_ok = next((q for q in query_status if q == 1), True)
            except (IndexError, KeyError, PermissionError,
                    psycopg2.OperationalError):
                cls.__show_exception()
        return inserts_ok

    @classmethod
    def process_data(cls, input_path: pathlib.Path) -> bool:
        """Locates source JSON files recursively from input path."""
        status = False
        if isinstance(input_path, pathlib.Path) and input_path:
            try:
                file_path_list = [p.absolute() for p in
                                  sorted(input_path.rglob("*.json"))
                                  if p.is_file()]
                print(f"{len(file_path_list)} files found in "
                      f"'{os.sep.join(input_path.parts[-3:])}'")
                for idx, json_path in enumerate(file_path_list, 0):
                    cls.process_file(json_path)
                    print(f"  processing: file_{idx:02d}: {json_path.name}")
                if len(file_path_list) > 0:
                    status = True
            except (OSError, PermissionError, KeyError):
                cls.__show_exception()
        return status

    @classmethod
    def close(cls):
        cls.db_cur.close()
        cls.db_conn.close()
