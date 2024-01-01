import json
import urllib.parse
import requests

from tools.logger.logger import log
from catalog.src_modules.tmdb.config import TMDB_API_BASE_URI, TMDB_API_VERSION, TMDB_POSTER_SIZE_INDEX

POPULARITY_COUNT_MIN = 2
VOTE_COUNT_MIN = 5


class TMDBError(Exception):
    pass


class TMDBResponse:
    def __init__(self):
        self.id = None
        self.text = None
        self.json = None
        self.status_code = None
        self.err = None
        self.resource_name = None

    def clear(self):
        self.id = None
        self.text = None
        self.json = None
        self.status_code = None
        self.err = None
        self.resource_name = None

    def set_state(self, response):
        self.text = response.text
        self.json = response.json()
        self.status_code = response.status_code
        self.id = self.json.get('id')

    def __str__(self):
        return (f"Id: {self.id}\n"
                f"Id: {self.id}\n"
                )


class TMDBClient:
    def __init__(self, api_token):
        self.api_token = api_token
        self.base_uri = f"{TMDB_API_BASE_URI}/{TMDB_API_VERSION}"
        self.url = None
        self.headers = None
        self.response = TMDBResponse()
        self.configuration = None
        self.im_base_uri = None
        self.poster_size = None

        self._init()
        self._get_configuration()

    def _init(self):
        self.headers = {
            'Authorization': f"Bearer {self.api_token}",
            'Content-Type': 'application/json'
            }

    def _get_configuration(self):
        self.url = f"{self.base_uri}/configuration"
        log.info(f"Request GET {self.url}")
        self._get_response()
        self.configuration = self.response.json
        if self.configuration:
            self.im_base_uri = self.configuration['images']['secure_base_url']
            self.poster_size = self.configuration['images']['poster_sizes'][TMDB_POSTER_SIZE_INDEX]
        return self.configuration

    def _get_response(self):
        try:
            response = requests.get(self.url, headers=self.headers)
            self.response.set_state(response)
            return self.response
        except Exception as e:
            raise TMDBError(f"Error getting TMDB answer! Msg: {e}")

    def get_resource_info(self, resource, id_):
        self.response.clear()
        self.response.resource_name = resource
        self.url = f"{self.base_uri}/{resource}/{id_}"
        log.info(f"Request GET {self.url}")
        return self._get_response()

    def get_resource_images(self, resource, id_):
        self.response.clear()
        self.response.resource_name = resource
        self.url = f"{self.base_uri}/{resource}/{id_}/images"
        log.info(f"Request GET {self.url}")
        return self._get_response()

    def get_movie_info(self, id_):
        return self.get_resource_info('movie', id_)

    def get_movie_images(self, id_):
        return self.get_resource_images('movie', id_)

    def get_person_info(self, id_):
        return self.get_resource_info('person', id_)

    def get_person_images(self, id_):
        return self.get_resource_images('person', id_)

    def get_search_resource(self, resource, name, filter_):
        self.response.clear()
        self.response.resource_name = resource
        name = urllib.parse.quote(name)
        self.url = (f"{self.base_uri}/{'search'}/{resource}"
                    f"?query={name}"
                    f"&{filter_}")
        log.info(f"Request GET {self.url}")
        return self._get_response()

    def get_search_movie(self, name, filter_=''):
        return self.get_search_resource('movie', name=name, filter_=filter_)

    def get_search_person(self, name, filter_=''):
        return self.get_search_resource('person', name=name, filter_=filter_)

    def get_discover_resource(self, resource, filter_):
        self.response.clear()
        self.response.resource_name = resource
        filter_ = urllib.parse.quote(filter_)
        self.url = (f"{self.base_uri}/{'discover'}/{resource}"
                    f"?{filter_}")
        log.info(f"Request GET {self.url}")
        return self._get_response()

    def get_discover_movie(self, filter_=''):
        return self.get_discover_resource('movie', filter_=filter_)

    def filter_response(self, filter_count_min=None):
        if self.response.status_code != 200:
            return

        filter_count_key = 'vote_count' if self.response.resource_name == 'movie' else 'popularity'
        if not filter_count_min:
            filter_count_min = VOTE_COUNT_MIN if self.response.resource_name == 'movie' else POPULARITY_COUNT_MIN

        movies_json = [movie for movie in self.response.json['results']
                       if movie[filter_count_key] >= filter_count_min]
        self.response.json['results'] = movies_json
        self.response.json['total_results_not_filtered'] = self.response.json['total_results']
        self.response.json['total_results'] = len(movies_json)
        self.response.text = json.dumps(self.response.json)

    def get_full_image_path(self, image_path):
        if not image_path:
            return ''
        return f"{self.im_base_uri}{self.poster_size}{image_path}"


if __name__ == '__main__':
    from catalog.src_modules.tmdb.config import TMDB_API_TOKEN_FILE_NAME
    from tools.utils import utils

    client = TMDBClient(api_token=utils.read_file_as_string(TMDB_API_TOKEN_FILE_NAME))

    client.get_movie_info(id_=16905)
    log.info(client.response.text)

    client.get_movie_images(id_=80364)
    log.info(client.response.text)

    client.get_person_info(id_=8724)
    log.info(client.response.text)

    client.get_person_images(id_=30210)
    log.info(client.response.text)

    client.get_search_movie(
        name="Captain Blood",
        filter_="year=1935"
                "&include_adult=false&language=en-US")
    client.filter_response()
    log.info(client.response.text)

    client.get_search_person(
        name="Jean Arthur",
        filter_="include_adult=false&language=en-US")
    client.filter_response()
    log.info(client.response.text)

    client.get_discover_movie(
        filter_="year>=1932&year<=1950"
                "&include_adult=false&include_video=false&language=en-US"
                "&with_cast=Errol%20Flynn"
                "&sort_by=popularity.desc")
    client.filter_response(filter_count_min=0.2)
    log.info(client.response.text)
