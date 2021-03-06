# -*- coding: UTF-8 -*-
"""Media driver module to insert JSON media tag data into PostgreSQL."""
import os
import pathlib
import time
from db import cmd_args
from db import postgres_api
from db import postgres_select_queries as sql

BASE_DIR, MODULE_NAME = os.path.split(os.path.abspath(__file__))
PARENT_PATH, CURR_DIR = os.path.split(BASE_DIR)
TWO_PARENT_PATH = os.sep.join(pathlib.Path(BASE_DIR).parts[:-2])
DEMO_ENABLED = True
PRIVATE_CONFIG = False


def main():
    """Driver to generate Postgres database records from JSON source file."""
    print(f"{MODULE_NAME} starting...")
    start = time.perf_counter()
    args = cmd_args.get_cmd_args(port_num=5432)
    server = args.server
    port_num = args.port_num
    database = args.database
    username = args.username
    password = args.password
    pg_api = postgres_api.PostgresMedia(hostname=server,
                                        port_num=port_num,
                                        username=username,
                                        password=password,
                                        db_name=database,
                                        private_cfg=PRIVATE_CONFIG)
    if pg_api.is_connected():
        pg_api.drop_tables()
        pg_api.create_tables()
        json_path = pathlib.Path(PARENT_PATH, 'data', 'input')
        pg_api.process_data(json_path)
        pg_api.show_database_status()
        if DEMO_ENABLED:
            pg_api.query(query=sql.ARTIST_SELECT, params=['Mazzy Star'])
            pg_api.query(query=sql.ALBUM_SELECT, params=['Debut'])
            pg_api.query(query=sql.TRACK_SELECT, params=['Future Proof'])
            pg_api.query(query=sql.GENRE_SELECT, params=['Classical'])
            pg_api.query(query=sql.FILE_SELECT, params=['.flac'])
            pg_api.query(query=sql.GAIN_SELECT, params=['-4.0'])
            pg_api.query(query=sql.JOIN_SELECT, params=['Rockabilly'])
            pg_api.query(query=sql.AVG_SIZE_SELECT)
        pg_api.close()
    end = time.perf_counter() - start
    print(f"\n{MODULE_NAME} finished in {end:0.2f} seconds")


if __name__ == "__main__":
    main()
