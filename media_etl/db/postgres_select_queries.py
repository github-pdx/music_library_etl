# -*- coding: UTF-8 -*-
"""Select queries for PostgreSQL."""
ARTIST = "artist"
ALBUM = "album"
TRACK = "track"
GENRE = "genre"
FILE_META = "filedata"

ARTIST_SELECT = (f"SELECT * FROM {ARTIST} "
                 f"WHERE artist = (%s)")

ALBUM_SELECT = (f"SELECT * FROM {ALBUM} "
                f"WHERE album = (%s)")

TRACK_SELECT = (f"SELECT * FROM {TRACK} "
                f"WHERE title = (%s)")

TRACK_SELECT2 = ("SELECT s.track_id, a.artist_id "
                 "FROM track t "
                 "JOIN artist a "
                 "ON t.artist_id = a.artist_id "
                 "WHERE s.title = (%s) and "
                 "a.artist = (%s) and t.track_length = (%s);")

GENRE_SELECT = (f"SELECT * FROM {GENRE} "
                f"WHERE genre = (%s)")
FILE_SELECT = (f"SELECT file_name, readable_size FROM {FILE_META} "
               f"WHERE file_ext = (%s)")
