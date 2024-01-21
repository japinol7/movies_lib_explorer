import os

from collections import namedtuple, OrderedDict

from config.config import (
    ROOT_FOLDER,
    RESOURCES_FOLDER,
    STR_ENCODING,
    ERROR_PERMISSION_MSG,
    LOGGER_FORMAT
    )

API_VERSION = 1
API_DIRECTORS_PATH = f'api/v{API_VERSION}/directors'
API_MOVIES_PATH = f'api/v{API_VERSION}/movies'
API_ACTORS_PATH = f'api/v{API_VERSION}/actors'
API_AUTH_TOKEN_PATH = f'api/v{API_VERSION}/token-auth'

SETTINGS_ID = 1
DEFAULT_MOVIES_LIST_LIMIT = 2500
DEFAULT_PEOPLE_LIST_LIMIT = 1000
MAX_MOVIES_LIST_LIMIT = 3000
MAX_PEOPLE_LIST_LIMIT = 3000

config_settings = {'settings': None}

MOVIE_YEAR_MIN = 1900
MOVIE_YEAR_MAX = 2099
TIME_SLEEP_WHEN_FEED_CONTENT = 0


MOVIE_GENRES = [
    'Action',
    'Adventure',
    'Animation',
    'Comedy',
    'Crime',
    'Documentary',
    'Drama',
    'Fantasy',
    'History',
    'Horror',
    'Mystery',
    'Music',
    'Science Fiction',
    'Romance',
    'Thriller',
    'TV Movie',
    'War',
    'Western',
    ]

DATASET_SOURCE_FORMAT = 'csv'

DELIMITER_CSV = ','
DECIMAL_SEPARATOR_CSV = '.'
THOUSANDS_SEPARATOR_CSV = '.' if DECIMAL_SEPARATOR_CSV == ',' else ','

DATASET_FOLDER = os.path.join(ROOT_FOLDER, 'resources', 'data')
DATASET_FOLDER_ZIP = os.path.join(DATASET_FOLDER, 'zip')
DATASET_FILE_ZIP = os.path.join(DATASET_FOLDER_ZIP, 'data.zip')

DELIMITER = '.||.'
LANGUAGE_WRAPPER = '||'

MOVIE_DATASET_FILE_NAME = 'main_catalog_movie'
MOVIE_DATASET_FILE = os.path.join(DATASET_FOLDER, f'{MOVIE_DATASET_FILE_NAME}.{DATASET_SOURCE_FORMAT}')

DIRECTOR_DATASET_FILE_NAME = 'main_catalog_director'
DIRECTOR_DATASET_FILE = os.path.join(DATASET_FOLDER, f'{DIRECTOR_DATASET_FILE_NAME}.{DATASET_SOURCE_FORMAT}')

ACTOR_DATASET_FILE_NAME = 'main_catalog_actor'
ACTOR_DATASET_FILE = os.path.join(DATASET_FOLDER, f'{ACTOR_DATASET_FILE_NAME}.{DATASET_SOURCE_FORMAT}')

DATASET_SOURCE_CSV = 'csv'
DATASET_SOURCE_JSON = 'json'

MovieColumnsMapping = namedtuple('movie_columns_mapping', [DATASET_SOURCE_CSV, DATASET_SOURCE_JSON])
MOVIE_COLUMNS_MAPPING = OrderedDict({
    'id': MovieColumnsMapping('id', 'id'),
    'title': MovieColumnsMapping('title', 'title'),
    'year': MovieColumnsMapping('year', 'year'),
    'created': MovieColumnsMapping('created', 'created'),
    'updated': MovieColumnsMapping('updated', 'updated'),
    'director_id': MovieColumnsMapping('director_id', 'directorId'),
    'cast': MovieColumnsMapping('cast', 'cast'),
    'country': MovieColumnsMapping('country', 'country'),
    'description': MovieColumnsMapping('description', 'description'),
    'language': MovieColumnsMapping('language', 'language'),
    'note': MovieColumnsMapping('note', 'note'),
    'production_company': MovieColumnsMapping('production_company', 'productionCompany'),
    'runtime': MovieColumnsMapping('runtime', 'runtime'),
    'title_original': MovieColumnsMapping('title_original', 'titleOriginal'),
    'cinematography': MovieColumnsMapping('cinematography', 'cinematography'),
    'genres': MovieColumnsMapping('genres', 'genres'),
    'producer': MovieColumnsMapping('producer', 'producer'),
    'writer': MovieColumnsMapping('writer', 'writer'),
    })

MOVIE_COLUMN_TO_GROUP_BY = 'director_id_and_title'

MovieColumnToAddToGroup = namedtuple('movie_column_to_add_to_group', ['new_column', 'column1', 'column2'])
MOVIE_COLUMN_TO_ADD_TO_GROUP = MovieColumnToAddToGroup('director_id_and_title', 'director_id', 'title')

DirectorColumnsMapping = namedtuple('director_columns_mapping', [DATASET_SOURCE_CSV, DATASET_SOURCE_JSON])
DIRECTOR_COLUMNS_MAPPING = OrderedDict({
    'id': MovieColumnsMapping('id', 'id'),
    'last_name': MovieColumnsMapping('last_name', 'lastName'),
    'first_name': MovieColumnsMapping('first_name', 'firstName'),
    'created': MovieColumnsMapping('created', 'created'),
    'updated': MovieColumnsMapping('updated', 'updated'),
    })

DIRECTOR_COLUMN_TO_GROUP_BY = 'id_and_last_name'

DirectorColumnToAddToGroup = namedtuple('director_column_to_add_to_group', ['new_column', 'column1', 'column2'])
DIRECTOR_COLUMN_TO_ADD_TO_GROUP = DirectorColumnToAddToGroup('id_and_last_name', 'id', 'last_name')

ActorColumnsMapping = namedtuple('actor_columns_mapping', [DATASET_SOURCE_CSV, DATASET_SOURCE_JSON])
ACTOR_COLUMNS_MAPPING = OrderedDict({
    'id': MovieColumnsMapping('id', 'id'),
    'last_name': MovieColumnsMapping('last_name', 'lastName'),
    'first_name': MovieColumnsMapping('first_name', 'firstName'),
    'created': MovieColumnsMapping('created', 'created'),
    'updated': MovieColumnsMapping('updated', 'updated'),
    })

ACTOR_COLUMN_TO_GROUP_BY = 'id_and_last_name'

ActorColumnToAddToGroup = namedtuple('actor_column_to_add_to_group', ['new_column', 'column1', 'column2'])
ACTOR_COLUMN_TO_ADD_TO_GROUP = ActorColumnToAddToGroup('id_and_last_name', 'id', 'last_name')

DATE_COLUMNS = []
AMOUNT_COLUMNS = []
COLUMNS_TO_STRIP_WHITESPACE_FROM = ['title']

MOVIES_EXPORT_FILE_NAME = 'movies_report.xlsx'

MOVIES_EXPORT_FIELD_NORMAL_WIDTH = 22
movies_export_field_titles = namedtuple('movies_export_field_titles', ['name', 'width'])
MOVIES_EXPORT_FIELD_TITLES = [
    movies_export_field_titles('id', 12),
    movies_export_field_titles('title', 49),
    movies_export_field_titles('year', 9),
    movies_export_field_titles('runtime', 9.5),
    movies_export_field_titles('director', 28),
    movies_export_field_titles('genres', 64),
    movies_export_field_titles('country', 9.5),
    movies_export_field_titles('language', 19),
    movies_export_field_titles('decade', 9),
    movies_export_field_titles('title_original', 52),
    movies_export_field_titles('cast', 104),
    movies_export_field_titles('description', 65),
    movies_export_field_titles('note', 44),
    movies_export_field_titles('director_id', 12),
    movies_export_field_titles('director_fn', MOVIES_EXPORT_FIELD_NORMAL_WIDTH),
    movies_export_field_titles('director_ln', MOVIES_EXPORT_FIELD_NORMAL_WIDTH),
    movies_export_field_titles('production_company', MOVIES_EXPORT_FIELD_NORMAL_WIDTH),
    movies_export_field_titles('cinematography', MOVIES_EXPORT_FIELD_NORMAL_WIDTH),
    movies_export_field_titles('picture', 70),
    movies_export_field_titles('producer', MOVIES_EXPORT_FIELD_NORMAL_WIDTH),
    movies_export_field_titles('writer', MOVIES_EXPORT_FIELD_NORMAL_WIDTH),
    movies_export_field_titles('created', 14),
    movies_export_field_titles('updated', 14),
    ]
EXPORT_FILE_PROPERTIES = {
    'title': 'Movie list report from MLME',
    'subject': 'Movie list report from MLME',
    'author': 'Movies Library Metadata Explorer - MLME',
    'keywords': 'movie, MLME',
    'comments': 'Created with Movies Library Metadata Explorer - MLME using XlsxWriter',
    }


def update_config_settings(settings_model):
    try:
        settings = settings_model.objects.get(id=SETTINGS_ID)
    except settings_model.DoesNotExist:
        settings = settings_model.objects.create(
            id=SETTINGS_ID,
            movies_list_limit=DEFAULT_MOVIES_LIST_LIMIT,
            people_list_limit=DEFAULT_PEOPLE_LIST_LIMIT,
        )

    config_settings['settings'] = settings
    return settings
