from zipfile import ZipFile

from config import config
from tools.dataset.csv_dataset import CsvDataset
from tools.logger.logger import log

from catalog.models.movie import Movie
from catalog.models.director import Director


class ImportDataException(Exception):
    pass


def import_initial_data():
    data = {
        'movies': Movie.objects.order_by('title', 'director__last_name', 'director__first_name', 'year'),
        'directors': Director.objects.order_by('last_name', 'first_name'),
        }
    if data['movies'] or data['directors']:
        log.info("Skip import data. There is already data in the dabatase.")
        return

    __unzip_data_files()
    __import_catalog_directors()
    __import_catalog_movies()


def __unzip_data_files():
    log.info(f"Unzip database files")
    try:
        with ZipFile(config.DATASET_FILE_ZIP) as fin_zip:
            fin_zip.extractall(config.RESOURCES_FOLDER)
    except FileNotFoundError:
        raise ImportDataException(f"Error extracting database files. File not found: {config.DATASET_FILE_ZIP}")
    except Exception as e:
        raise ImportDataException(f"Error extracting database files from: {config.DATASET_FILE_ZIP}. Error msg: {e}")


def __get_dataset_from_csv(dataset_file_name, columns_mapping, column_to_add_to_group, column_to_group_by):
    with open(dataset_file_name, 'r', encoding='utf8') as fin:
        data = fin.read()
    return CsvDataset(data, columns_mapping, column_to_add_to_group).get_grouped(column_to_group_by)


def __get_dataset_from_json(dataset_file_name, columns_mapping, column_to_add_to_group, column_to_group_by):
    with open(dataset_file_name, 'r', encoding='utf8') as fin:
        data = fin.read()
    return CsvDataset(data, columns_mapping, column_to_add_to_group).get_grouped(column_to_group_by)


def __import_catalog_movies():
    log.info(f"Start to Import movie lib movies file")
    if config.DATASET_SOURCE_FORMAT == config.DATASET_SOURCE_CSV:
        dataset = __get_dataset_from_csv(config.MOVIE_DATASET_FILE,
                                         config.MOVIE_COLUMNS_MAPPING,
                                         config.MOVIE_COLUMN_TO_ADD_TO_GROUP,
                                         config.MOVIE_COLUMN_TO_GROUP_BY)
    elif config.DATASET_SOURCE_FORMAT == config.DATASET_SOURCE_JSON:
        dataset = __get_dataset_from_json(config.MOVIE_DATASET_FILE,
                                          config.MOVIE_COLUMNS_MAPPING,
                                          config.MOVIE_COLUMN_TO_ADD_TO_GROUP,
                                          config.MOVIE_COLUMN_TO_GROUP_BY)
    else:
        raise ImportDataException(f"Internal Error extracting database files. "
                                  f"Source Format not supported: {config.DATASET_SOURCE_FORMAT}")

    count_movies = 0
    for key, rows in dataset:
        if not key:
            continue
        count_movies += 1
        vals = list(rows)[0]
        log.info(f"Adding movie num {count_movies:6} to database: {key}")
        director = Director.objects.get(id=vals['director_id'])
        del vals[config.MOVIE_COLUMN_TO_GROUP_BY]
        vals['director_id'] = director.id
        Movie.objects.create(**vals)
    log.info("Committing to database")
    log.info(f"End Import movie lib movies file")


def __import_catalog_directors():
    log.info(f"Start to Import movie lib directors file")
    if config.DATASET_SOURCE_FORMAT == config.DATASET_SOURCE_CSV:
        dataset = __get_dataset_from_csv(config.DIRECTOR_DATASET_FILE,
                                         config.DIRECTOR_COLUMNS_MAPPING,
                                         config.DIRECTOR_COLUMN_TO_ADD_TO_GROUP,
                                         config.DIRECTOR_COLUMN_TO_GROUP_BY)
    elif config.DATASET_SOURCE_FORMAT == config.DATASET_SOURCE_JSON:
        dataset = __get_dataset_from_json(config.DIRECTOR_DATASET_FILE,
                                          config.DIRECTOR_COLUMNS_MAPPING,
                                          config.DIRECTOR_COLUMN_TO_ADD_TO_GROUP,
                                          config.DIRECTOR_COLUMN_TO_GROUP_BY)
    else:
        raise ImportDataException(f"Internal Error extracting database files. "
                                  f"Source Format not supported: {config.DATASET_SOURCE_FORMAT}")

    count_directors = 0
    for key, rows in dataset:
        if not key:
            continue
        count_directors += 1
        vals = list(rows)[0]
        del vals[config.DIRECTOR_COLUMN_TO_GROUP_BY]
        log.info(f"Adding director num {count_directors:6} to database: {key}")
        Director.objects.create(**vals)
    log.info("Committing to database")
    log.info(f"End Import director lib directors file")
