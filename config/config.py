import os
import pathlib

from collections import namedtuple, OrderedDict

LOGGER_FORMAT = '%(levelname)s: %(message)s'
STR_ENCODING = 'utf-8'

DATASET_SOURCE_FORMAT = 'csv'

DELIMITER_CSV = ','
DECIMAL_SEPARATOR_CSV = '.'
THOUSANDS_SEPARATOR_CSV = '.' if DECIMAL_SEPARATOR_CSV == ',' else ','

ROOT_FOLDER = pathlib.Path(__file__).parent.parent
RESOURCES_FOLDER = os.path.join(ROOT_FOLDER, 'resources')
DATASET_FOLDER = os.path.join(ROOT_FOLDER, 'resources', 'data')
DATASET_FOLDER_ZIP = os.path.join(DATASET_FOLDER, 'zip')
DATASET_FILE_ZIP = os.path.join(DATASET_FOLDER_ZIP, 'data.zip')

DELIMITER = '.||.'
LANGUAGE_WRAPPER = '||'

MOVIE_DATASET_FILE_NAME = 'main_catalog_movie'
MOVIE_DATASET_FILE = os.path.join(DATASET_FOLDER, f'{MOVIE_DATASET_FILE_NAME}.{DATASET_SOURCE_FORMAT}')

DIRECTOR_DATASET_FILE_NAME = 'main_catalog_director'
DIRECTOR_DATASET_FILE = os.path.join(DATASET_FOLDER, f'{DIRECTOR_DATASET_FILE_NAME}.{DATASET_SOURCE_FORMAT}')

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

DATE_COLUMNS = []
AMOUNT_COLUMNS = []
COLUMNS_TO_STRIP_WHITESPACE_FROM = ['title']
