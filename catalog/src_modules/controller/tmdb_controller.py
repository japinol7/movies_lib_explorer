from functools import lru_cache

from catalog.src_modules.tmdb.config import (
    TMDB_API_TOKEN_FILE_NAME,
    TMDB_API_BASE_URI,
    TMDB_WEBSITE_URI,
    TMDB_API_VERSION,
    TMDB_ATTRIBUTION_NOTICE,
    )
from catalog.src_modules.tmdb.tmdb_client import TMDBClient
from tools.logger.logger import log
from tools.utils import utils

TMDB_API_LRU_CACHE_SIZE = 32
TMDB_CONNECTOR_INFO = {
    'tmdb_connector_title': 'TMDB Connector Integration',
    'tmdb_connector_api_uri': TMDB_API_BASE_URI,
    'tmdb_connector_website_uri': TMDB_WEBSITE_URI,
    'tmdb_connector_api_version': TMDB_API_VERSION,
    'tmdb_connector_attribution_notice': TMDB_ATTRIBUTION_NOTICE,
    'tmdb_connector_body': 'Search data on TMDB website:',
    }


class TMDBController:
    def __init__(self):
        self.id = None
        self.client = None
        self.tmdb_errors = []

    def get_client(self):
        self.tmdb_errors = []
        try:
            self.client = TMDBClient(api_token=utils.read_file_as_string(TMDB_API_TOKEN_FILE_NAME))
        except Exception as e:
            log.error(f"TMDB. Error while getting TMDB client: {e}")
            self.tmdb_errors += ["ERROR. You need a valid TMDB API token to use this feature"]

        return self.client

    def _is_client_set(self):
        if not self.client:
            log.error("No TMDB client")
            return False
        return True

    @staticmethod
    @lru_cache(maxsize=TMDB_API_LRU_CACHE_SIZE)
    def _get_search_movie(client, name, filter_):
        client.get_search_movie(name, filter_)
        client.filter_response()
        data = client.response.json['results']

        # Get full poster path and movie details
        for movie in data:
            movie['mlde_im_poster_uri'] = client.get_full_image_path(movie['poster_path'])
            movie['mlde_is_orig_title_diff'] = movie['title'] != movie['original_title']
            client.get_movie_info(movie['id'])
            movie_details = client.response.json
            movie['mlde_genres'] = ', '.join(sorted([genre['name'] for genre in movie_details['genres']]))
            movie['mlde_runtime'] = movie_details['runtime']

        log.info(data)
        return data

    def get_search_movie(self, name, filter_):
        log.info(f"TMDB. Search movie with title: {name} | filter: {filter_}")
        if not self._is_client_set():
            return
        return self.__class__._get_search_movie(self.client, name, filter_)

    @staticmethod
    @lru_cache(maxsize=TMDB_API_LRU_CACHE_SIZE)
    def _get_search_person(client, name, filter_):
        client.get_search_person(name, filter_)
        client.filter_response()
        data = client.response.json['results']

        # Get full image path and person details
        for person in data:
            person['mlde_im_profile_uri'] = client.get_full_image_path(person['profile_path'])
            person['mlde_is_orig_name_diff'] = person['name'] != person['original_name']
            client.get_person_info(person['id'])
            person_details = client.response.json
            person['mlde_birth_date'] = person_details['birthday'] or ''
            person['mlde_death_date'] = person_details['deathday'] or ''
            person['mlde_birth_place'] = person_details['place_of_birth'] or ''
            person['mlde_biography'] = person_details['biography'] or ''
    
        log.info(data)
        return data

    def get_search_person(self, name, filter_):
        log.info(f"TMDB. Search person with name: {name} | filter: {filter_}")
        if not self._is_client_set():
            return
        return self.__class__._get_search_person(self.client, name, filter_)
