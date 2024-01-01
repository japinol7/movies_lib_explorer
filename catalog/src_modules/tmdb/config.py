import os
from pathlib import Path

TMDB_API_BASE_URI = "https://api.themoviedb.org"
TMDB_WEBSITE_URI = "https://www.themoviedb.org"
TMDB_ATTRIBUTION_NOTICE = "This product uses the TMDB API but is not endorsed or certified by TMDB."

TMDB_API_VERSION = 3
TMDB_API_KEY_FOLDER_NAME = os.path.join(str(Path.home()), '.api_keys', 'tmdb_api_keys')
TMDB_API_TOKEN_FILE_NAME = os.path.join(TMDB_API_KEY_FOLDER_NAME, 'tmdb_read_access_token.key')

TMDB_POSTER_SIZE_INDEX = 4
