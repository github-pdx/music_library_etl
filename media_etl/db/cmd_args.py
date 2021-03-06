# -*- coding: UTF-8 -*-
"""UI module to parse user input."""
import argparse
import inspect
import os
import pathlib
from pathvalidate.argparse import sanitize_filepath_arg

BASE_DIR, MODULE_NAME = os.path.split(os.path.abspath(__file__))
PARENT_PATH, CURR_DIR = os.path.split(BASE_DIR)
TWO_PARENT_PATH = os.sep.join(pathlib.Path(BASE_DIR).parts[:-2])

__all__ = ['get_cmd_args']


def get_cmd_args(port_num: int = 5432) -> list:
    """Command line input on directory to scan recursively for media files."""
    def_name = inspect.currentframe().f_code.co_name
    parser = argparse.ArgumentParser(description='media_db_parser')
    parser.add_argument("-s", "--server",
                        type=str, default='localhost',
                        help="server ip address or hostname")
    parser.add_argument("-p", "--port_num",
                        type=int, default=port_num,
                        help="port_num")
                        # 5433 5432 27017 27018
    parser.add_argument("-d", "--database",
                        type=str, default='media_db',
                        help="database name")
    parser.add_argument("-i", "--input_path",
                        type=sanitize_filepath_arg,
                        help="input file path")
    parser.add_argument("-u", "--username",
                        type=str, default='run_admin_run',
                        help="username")
    parser.add_argument("-w", "--password",
                        type=str, default='run_pass_run',
                        help="password")
    args = parser.parse_args()
    if args.input_path is None:
        args.input_path = pathlib.Path(TWO_PARENT_PATH, 'data', 'input')
    else:
        args.input_path = pathlib.Path(args.input_path)
        if args.input_path.exists() and args.file_path.is_dir():
            print(f"{def_name}() dumping path:'{str(args.input_path)}'")
        else:
            parser.error(f"invalid path: '{str(args.input_path)}'")
            args.input_path = None
    return args