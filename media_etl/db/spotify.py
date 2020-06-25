# -*- coding: UTF-8 -*-
"""Spotify API client to lookup tag data."""
import os
import pathlib
import sys
import configparser
import traceback
import spotipy
from rapidfuzz import fuzz
from spotipy.oauth2 import SpotifyClientCredentials

BASE_DIR, MODULE_NAME = os.path.split(os.path.abspath(__file__))
TWO_PARENT_PATH = os.sep.join(pathlib.Path(BASE_DIR).parts[:-2])
DEGUB = False

OFFLINE_ARTIST_IDS = {'Arcade Fire': '3kjuyTCjPG1WMFCiyc5IuB',
                      'Frank Sinatra': '1Mxqyy3pSjf8kZZL4QVxS0',
                      'Interpol': '3WaJSfKnzc65VDgmj2zU8B',
                      'Rimsky-Korsakov': '2kXJ68O899XvWOBdpzlXgs',
                      'M. Ward': '6nXSnNEdLuKTzAQozRtqiI',
                      'Massive Attack': '6FXMGgJwohJLUSr5nVlf9X',
                      'Mazzy Star': '37w38cCSGgKLdayTRjna4W',
                      'Ravel': '17hR0sYHpx7VYTMRfFUOmY',
                      'Beethoven': '2wOqMjp9TyABvtHdOSOTUS',
                      'Björk': '7w29UYBi0qsHi5RTcv3lmA',
                      'Patsy Cline': '7dNsHhGeGU5MV01r06O8gK',
                      'Sallie Ford & The Sound Outside': '0Z8RhQLJrLxKMWoUW2qo95'}

OFFLINE_ALBUM_IDS = {'The Suburbs': '3DrgM5X3yX1JP1liNLAOHI',
                     'Sinatra Reprise': '4Rka7iTWRtRUFouxyzEKKV',
                     'Turn On The Bright Lights': '79deKDaslwLfH3yPR2T3SB',
                     'Capriccio Espagnol': '4aIDs5QPfX9T7SdPIXOwVL',
                     'Hold Time': '4C8AUW89DL5LE5ikBBm4sp',
                     '100th Window': '60szvcndZTCqG9E7GSAplB',
                     'So Tonight That I Might See': '5K18gTgac0q6Jma5HkV1vA',
                     'Rapsodie Espagnol': '2tVaOSl5WI3hfTLMmkxcWs',
                     'Symphony No.8 in F-major, Op.93': '7w29UYBi0qsHi5RTcv3lmA',
                     'Debut': '3icT9XGrBfhlV8BKK4WEGX',
                     'Definitive Collection': '3g5uyAp8sS8LnnCxh9y2em',
                     'Dirty Radio': '7I9KroNPmpw9qFYZ8Vp7pN'}


class ConfigClient:
    """ConfigParser Class to parse Spotify config file."""

    @classmethod
    def __init__(cls, config_path: pathlib.Path):
        """Start ConfigParser client to parse config file."""
        cls.__is_config_valid = False
        try:
            if config_path.exists() and config_path.is_file():
                cls.__cp = configparser.ConfigParser()
                cls.__cp.read(config_path)
                cls.__client_id = cls.__cp.get('spotify.com',
                                               'SPOTIPY_CLIENT_ID')
                cls.__client_secret = cls.__cp.get('spotify.com',
                                                   'SPOTIPY_CLIENT_SECRET')
                cls.__is_config_valid = True
            else:
                print(f"'{os.sep.join(config_path.parts[-3:])}' missing ")
        except (configparser.NoSectionError, configparser.Error,
                configparser.ParsingError):
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                                      limit=2, file=sys.stdout)

    @classmethod
    def is_config_valid(cls) -> bool:
        """Checks to see if spotify.cfg file exists and is valid."""
        return cls.__is_config_valid

    @classmethod
    def get_client_id(cls) -> str:
        """Returns Spoitfy API client id."""
        return cls.__client_id

    @classmethod
    def get_client_secret(cls) -> str:
        """Returns Spoitfy API client secret id."""
        return cls.__client_secret


class SpotifyClient:
    """Class to lookup/add Spotify media tags to Postgres backend."""

    @classmethod
    def __init__(cls, config_path: pathlib.Path):
        """Start Spotify API client to lookup tag data."""
        cls.__is_connected = False
        cls.__is_config_valid = False
        try:
            cls.__cc = ConfigClient(config_path)
            cls.__is_config_valid = cls.__cc.is_config_valid()
            if cls.__is_config_valid:
                cls.__client_id = cls.__cc.get_client_id()
                cls.__client_secret = cls.__cc.get_client_secret()
                cls.__scc = SpotifyClientCredentials(cls.__client_id,
                                                     cls.__client_secret)
                cls.__sp = spotipy.Spotify(
                    client_credentials_manager=cls.__scc)
                cls.bjork_urn = 'spotify:artist:7w29UYBi0qsHi5RTcv3lmA'
                cls.__sp.artist(cls.bjork_urn)
                cls.__is_connected = True
            else:
                print(f"invalid: '{os.sep.join(config_path.parts[-3:])}'")
        except spotipy.oauth2.SpotifyOauthError:
            print(f"\nexample: '{os.sep.join(config_path.parts[-3:])}': "
                  f"intentionally incorrect... using offline lookup")
        print(f"is_connected: {cls.is_connected()} "
              f"\tis_config_valid: {cls.is_config_valid()}")

    @staticmethod
    def __show_exception() -> None:
        """Custom traceback exception wrapper."""
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                  limit=2, file=sys.stdout)

    @classmethod
    def is_config_valid(cls) -> bool:
        """Checks to see if spotify.cfg file exists and is valid."""
        return cls.__is_config_valid

    @classmethod
    def is_connected(cls) -> bool:
        """Checks to see if spotify.cfg file exists and is valid."""
        return cls.__is_connected

    @classmethod
    def run_spotify(cls) -> bool:
        """If both client is connected adn spotify.cfg is valid."""
        return cls.is_config_valid() and cls.is_connected()

    @classmethod
    def get_artist_id(cls, artist_name: str) -> str:
        """Spotify API to lookup artist ID."""
        artist_id = ''
        if cls.run_spotify():
            try:
                results = cls.__sp.search(q=f"artist:{artist_name}",
                                          type='artist')
                items = results['artists']['items']
                if len(items) > 0:
                    artist_id = items[0]['id']
            except (spotipy.oauth2.SpotifyOauthError,
                    spotipy.exceptions.SpotifyException):
                cls.__show_exception()
        else:
            artist_id = OFFLINE_ARTIST_IDS[artist_name]
        print(f"   get_artist_id: {artist_name:32}\t{artist_id}")
        return artist_id

    @classmethod
    def get_album_id(cls, artist_id: str, target_album: str) -> str:
        """Spotify API to lookup album ID using rapidfuzz for closest match."""
        album_id = ''
        if cls.run_spotify():
            try:
                results = cls.__sp.artist_albums(artist_id=artist_id,
                                                 limit=50)
                albums = results['items']
                ratios = []
                for album in albums:
                    fuzz_ratio = round(fuzz.ratio(target_album.lower(),
                                                  album['name'].lower()), 4)
                    ratios.append(fuzz_ratio)
                # check album title by string similarity matching (rapidfuzz)
                max_idx = ratios.index(max(ratios))
                album_id = albums[max_idx]['id']
                if DEGUB:
                    print(f"album: {album['name']}\t"
                          f"id: {album['id']}\t ratio: {fuzz_ratio}")
                    print(f"idx: {max_idx} max:{max(ratios)}\n"
                          f"input_album:   {target_album}\n"
                          f"closest_album: {albums[max_idx]['name']}\n"
                          f"album_id:   {album_id}\n")
            except (spotipy.oauth2.SpotifyOauthError,
                    spotipy.exceptions.SpotifyException):
                cls.__show_exception()
        else:
            album_id = OFFLINE_ALBUM_IDS[target_album]
        print(f"    get_album_id: {target_album:32}\t{album_id}")
        return album_id
