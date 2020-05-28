# -*- coding: UTF-8 -*-
"""Tables and insert queries for PostgreSQL."""
ARTIST = "artist"
ALBUM = "album"
TRACK = "track"
GENRE = "genre"
FILE_META = "filedata"

TABLES = [ARTIST, ALBUM, TRACK, GENRE, FILE_META]

ARTIST_HEADERS = ['artist_id', 'artist_name', 'composer', 'conductor']
CREATE_ARTIST_QUERY = (f"CREATE TABLE IF NOT EXISTS {ARTIST} "
                       f"(id SERIAL PRIMARY KEY, "
                       f"artist_id VARCHAR(150) NULL, "
                       f"artist_name VARCHAR(150) NULL, "
                       f"composer VARCHAR(150) NULL, "
                       f"conductor VARCHAR(150) NULL);")

ALBUM_HEADERS = ['album_id', 'artist_id', 'album_title', 'year',
                 'album_gain', 'album_art']
CREATE_ALBUM_QUERY = (f"CREATE TABLE IF NOT EXISTS {ALBUM} "
                      f"(id SERIAL PRIMARY KEY, "
                      f"album_id VARCHAR(150) NULL, "
                      f"artist_id VARCHAR(150) NULL, "
                      f"album_title VARCHAR(200) NULL, "
                      f"year SMALLINT, "
                      f"album_gain NUMERIC(5,2), "
                      f"album_art VARCHAR(48) NULL);")

TRACK_HEADERS = ['track_id', 'album_title', 'track_title', 'track_number',
                 'track_length', 'artist_id', 'rating', 'comment',
                 'track_gain']
CREATE_TRACK_QUERY = (f"CREATE TABLE IF NOT EXISTS {TRACK} "
                      f"(id SERIAL PRIMARY KEY, "
                      f"track_id VARCHAR(150) NULL, "
                      f"album_title VARCHAR(200) NULL, "
                      f"track_title VARCHAR(200) NULL, "
                      f"artist_id VARCHAR(100) NULL, "
                      f"track_number SMALLINT, "
                      f"track_length VARCHAR(16) NULL, "
                      f"rating VARCHAR(16) NULL, "
                      f"comment VARCHAR(128) NULL, "
                      f"track_gain NUMERIC(5,2));")

GENRE_HEADERS = ['artist_id', 'artist_name', 'genre', 'genre_in_dict']
CREATE_GENRE_QUERY = (f"CREATE TABLE IF NOT EXISTS {GENRE} "
                      f"(id SERIAL PRIMARY KEY, "
                      f"artist_id VARCHAR(100) NULL, "
                      f"artist_name VARCHAR(100) NULL, "
                      f"genre VARCHAR(150) NULL, "
                      f"genre_in_dict VARCHAR(48) NULL);")

FILE_HEADERS = ['track_id', 'file_size', 'readable_size', 'file_ext',
                'encoder', 'file_name', 'path_len', 'last_modified',
                'encoding', 'hash']
CREATE_FILE_QUERY = (f"CREATE TABLE IF NOT EXISTS {FILE_META} "
                     f"(id SERIAL PRIMARY KEY, "
                     f"track_id VARCHAR(100) NULL, "
                     f"file_size INTEGER, "
                     f"readable_size VARCHAR(64) NULL, "
                     f"file_ext VARCHAR(16) NULL, "
                     f"encoder VARCHAR(64) NULL, "
                     f"file_name VARCHAR(256) NULL, "
                     f"path_len SMALLINT, "
                     f"last_modified TIMESTAMP, "
                     f"encoding VARCHAR(24) NULL, "
                     f"hash VARCHAR(150) NULL);")

HEADERS = {ARTIST: ARTIST_HEADERS, ALBUM: ALBUM_HEADERS, TRACK: TRACK_HEADERS,
           GENRE: GENRE_HEADERS, FILE_META: FILE_HEADERS}

CREATE_TABLES_QUERIES = [CREATE_ARTIST_QUERY, CREATE_ALBUM_QUERY,
                         CREATE_TRACK_QUERY,
                         CREATE_GENRE_QUERY, CREATE_FILE_QUERY]

ARTIST_INSERT = (f"INSERT INTO {ARTIST} "
                 "(artist_id, artist_name, composer, conductor) "
                 "VALUES (%s, %s, %s, %s);")

ALBUM_INSERT = (f"INSERT INTO {ALBUM} "
                "(album_id, artist_id, album_title, year, "
                "album_gain, album_art) "
                "VALUES (%s, %s, %s, %s, %s, %s);")

TRACK_INSERT = (f"INSERT INTO {TRACK} "
                "(track_id, album_title, track_title, track_number, "
                "track_length, artist_id, rating, comment, track_gain) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);")

GENRE_INSERT = (f"INSERT INTO {GENRE} "
                "(artist_id, artist_name, genre, genre_in_dict) "
                "VALUES (%s, %s, %s, %s);")

FILE_INSERT = (f"INSERT INTO {FILE_META} "
               "(track_id, file_size, readable_size, file_ext, "
               "encoder, file_name, path_len, last_modified, "
               "encoding, hash)"
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")

INSERTS = {ARTIST: ARTIST_INSERT, ALBUM: ALBUM_INSERT, TRACK: TRACK_INSERT,
           GENRE: GENRE_INSERT, FILE_META: FILE_INSERT}
