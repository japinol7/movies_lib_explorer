from zipfile import ZipFile

from django.db import models

from catalog.config import config
from tools.dataset.csv_dataset import CsvDataset
from tools.logger.logger import log

from catalog.models.movie import Movie
from catalog.models.director import Director
from catalog.models.actor import Actor


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
    __import_catalog_actors()
    __import_catalog_movies()
    __create_movie_actor_links()


def __create_movie_actor_links():
    data = get_data_to_update_actors_n_movie_actor_links()
    if data['movies']:
        update_actors_n_movie_actor_links(data)


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
    log.info("Start to Import movie lib movies file")
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
        raise ImportDataException("Internal Error extracting database files. "
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
        year = int(vals['year']) if vals['year'] and vals['year'].isnumeric() else 0
        vals['decade'] = _get_decade_from_year(year)
        vals['director_id'] = director.id
        Movie.objects.create(**vals)
    log.info("Committing to database")
    log.info("End Import movie lib movies file")


def _get_decade_from_year(year):
    return year - (year % 10) if 1900 <= year <= 9999 else 0


def __import_catalog_directors():
    log.info("Start to Import movie lib directors file")
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
    log.info("End Import director lib directors file")


def __import_catalog_actors():
    log.info("Start to Import movie lib actors file")
    if config.DATASET_SOURCE_FORMAT == config.DATASET_SOURCE_CSV:
        dataset = __get_dataset_from_csv(config.ACTOR_DATASET_FILE,
                                         config.ACTOR_COLUMNS_MAPPING,
                                         config.ACTOR_COLUMN_TO_ADD_TO_GROUP,
                                         config.ACTOR_COLUMN_TO_GROUP_BY)
    elif config.DATASET_SOURCE_FORMAT == config.DATASET_SOURCE_JSON:
        dataset = __get_dataset_from_json(config.ACTOR_DATASET_FILE,
                                          config.ACTOR_COLUMNS_MAPPING,
                                          config.ACTOR_COLUMN_TO_ADD_TO_GROUP,
                                          config.ACTOR_COLUMN_TO_GROUP_BY)
    else:
        raise ImportDataException(f"Internal Error extracting database files. "
                                  f"Source Format not supported: {config.DATASET_SOURCE_FORMAT}")

    count_actors = 0
    for key, rows in dataset:
        if not key:
            continue
        count_actors += 1
        vals = list(rows)[0]
        del vals[config.ACTOR_COLUMN_TO_GROUP_BY]
        log.info(f"Adding actor num {count_actors:6} to database: {key}")
        Actor.objects.create(**vals)
    log.info("Committing to database")
    log.info("End Import actor lib actors file")


def get_data_to_update_actors_n_movie_actor_links():
    return {
        'movies': Movie.objects.exclude(cast__isnull=True).exclude(cast__exact='').
                  exclude(actors__isnull=False).
                  order_by('title', 'director__last_name', 'director__first_name', 'year'),
        'actors': Actor.objects.order_by('last_name', 'first_name'),
        }


def update_actors_n_movie_actor_links(data):
    log.info("Start to create actors movie links")
    for movie in data['movies']:
        if not movie.cast:
            continue
        cast = movie.cast.replace('…', '').replace('...', '').replace('\n', '').\
            replace(', Jr.', ' __Jr.__').\
            replace(', Sr.', ' __Sr.__').split(',')
        cast = [actor.replace(' __Jr.__', ', Jr.').
                replace(' __Sr.__', ', Sr.').strip() for actor in cast]
        if cast and movie.actors.count() > 0:
            log.info(f"Clear movie previous actors: to the movie: {movie.id} {movie.title}")
            movie.actors.clear()

        for actor_name in cast:
            if actor_name.strip() == '':
                continue
            old_actors = Actor.objects.filter(
                models.Q(last_name=actor_name))
            actor_already_exists = old_actors.count() > 0
            if actor_already_exists:
                old_actor = old_actors[0]
                log.info(f"Add link to existing actor {old_actor.id} {old_actor.last_name} "
                         f"to the movie: {movie.id} {movie.title}")
                movie.actors.add(old_actor)
                continue
            vals = {
                'last_name': actor_name
                }
            new_actor = Actor.objects.create(**vals)
            new_actor.save()
            log.info(f"Add link to new actor {new_actor.id} {new_actor.last_name} "
                     f"to the movie: {movie.id} {movie.title}")
            movie.actors.add(new_actor)
