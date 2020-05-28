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

TRACK_SELECT = ("SELECT artist_id, album_title, "
                "track_title, track_length, rating "
                f"FROM {TRACK} "
                "WHERE track_title = (%s)")

GAIN_SELECT = ("SELECT m.album_gain, a.artist_name, t.album_title "
               f"FROM {TRACK} t "
               f"JOIN {ARTIST} a ON t.artist_id = a.artist_id "
               f"JOIN {ALBUM} m ON m.artist_id = a.artist_id "
               "WHERE m.album_gain <= (%s) "
               "ORDER BY m.album_gain DESC")

JOIN_SELECT = ("SELECT a.artist_name, t.album_title "
               f"FROM {ARTIST} a "
               f"JOIN {GENRE} g ON g.artist_id = a.artist_id "
               f"JOIN {TRACK} t ON t.artist_id = a.artist_id "
               "WHERE g.genre = (%s) "
               "ORDER BY artist_name")

GENRE_SELECT = (f"SELECT artist_name, genre "
                f"FROM {GENRE} "
                "WHERE genre = (%s)")

FILE_SELECT = ("SELECT file_name, encoding, file_ext "
               f"FROM {FILE_META} "
               "WHERE file_ext = (%s)")

AVG_SIZE_SELECT = f"SELECT AVG(file_size) FROM {FILE_META}"
