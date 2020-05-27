# -*- coding: UTF-8 -*-
"""Select queries for PostgreSQL."""
ARTIST = "artist"
ALBUM = "album"
TRACK = "track"
GENRE = "genre"
FILE_META = "filedata"

ARTIST_SELECT = ("SELECT artist_id, artist_name, composer, conductor "
                 f"FROM {ARTIST} "
                 "WHERE artist_name = (%s)")

ALBUM_SELECT = ("SELECT album_id, album_title, year, album_gain "
                f"FROM {ALBUM} "
                "WHERE album_title = (%s)")

TRACK_SELECT = ("SELECT artist_id, album_title, track_title, track_length, rating "
                f"FROM {TRACK} "
                "WHERE track_title = (%s)")

GAIN_SELECT = ("SELECT a.artist_name, t.album_title "
               f"FROM {TRACK} t "
               f"JOIN {ARTIST} a ON t.artist_id = a.artist_id "
               f"JOIN {ALBUM} b ON b.artist_id = a.artist_id "
               "WHERE b.album_gain <= (%s) "
               "ORDER BY b.album_gain ASC;")

JOIN_SELECT = ("SELECT a.artist_name, t.album_title "
               f"FROM {ARTIST} a "
               f"JOIN {GENRE} g ON g.artist_id = a.artist_id "
               f"JOIN {TRACK} t ON t.artist_id = a.artist_id "
               "WHERE g.genre = (%s) "
               "ORDER BY artist_name;")
            
GENRE_SELECT = (f"SELECT artist_name FROM {GENRE} "
                "WHERE genre = (%s);")

FILE_SELECT = ("SELECT file_name, encoding, file_ext " 
               f"FROM {FILE_META} "
               "WHERE file_ext = (%s)")
