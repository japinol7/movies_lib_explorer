import io
from datetime import datetime
import time

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import FileResponse
from django.shortcuts import render, get_object_or_404, redirect

import xlsxwriter

from catalog.config.config import (
    config_settings,
    update_config_settings,
    MOVIES_EXPORT_FIELD_TITLES,
    MOVIES_EXPORT_FILE_NAME,
    EXPORT_FILE_PROPERTIES,
    )
from catalog.forms.settings_forms import SettingsEditForm
from catalog.models.movie import Movie
from catalog.models.settings import Settings
from catalog.services.movie_services import set_movie_external_data_fields
from catalog.src_modules.controller.tmdb_controller import TMDBController
from tools.logger.logger import log

controller = TMDBController()


def catalog_settings(request):
    return render(
        request, 'catalog/settings.html',
        context={
            'data': config_settings['settings'],
            }
        )


@login_required
def settings_edit_form(request, settings_id):
    settings = get_object_or_404(Settings, id=settings_id)
    form = SettingsEditForm(instance=settings)

    if request.method == 'POST':
        if not request.user.is_staff:
            raise PermissionDenied("Permission Denied. You are not allowed to edit this model")
        form = SettingsEditForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            update_config_settings(Settings)
            return redirect('catalog:settings')

    return render(request, 'catalog/settings_edit_form.html',
                  {'settings': settings, 'form': form})


def _get_movies_export_field_values(movie, text_left__format, date_format):
    return [
        {'val': movie.id, 'format': None},
        {'val': movie.title, 'format': text_left__format},
        {'val': movie.year, 'format': None},
        {'val': movie.runtime, 'format': None},
        {'val': movie.director.first_name + ' ' + movie.director.last_name, 'format': text_left__format},
        {'val': movie.genres, 'format': text_left__format},
        {'val': movie.country, 'format': text_left__format},
        {'val': movie.language, 'format': text_left__format},
        {'val': movie.decade, 'format': None},
        {'val': movie.title_original, 'format': text_left__format},
        {'val': movie.cast, 'format': text_left__format},
        {'val': movie.description, 'format': text_left__format},
        {'val': movie.note, 'format': text_left__format},
        {'val': movie.director.id, 'format': None},
        {'val': movie.director.first_name, 'format': text_left__format},
        {'val': movie.director.last_name, 'format': text_left__format},
        {'val': movie.production_company, 'format': None},
        {'val': movie.cinematography, 'format': text_left__format},
        {'val': movie.ext_picture_uri, 'format': text_left__format},
        {'val': movie.picture.name, 'format': text_left__format},
        {'val': movie.producer, 'format': text_left__format},
        {'val': movie.writer, 'format': text_left__format},
        {'val': movie.created, 'format': date_format},
        {'val': movie.updated, 'format': date_format},
    ]


def _export_movies_report():
    log.info("Start exporting movies report")
    movies = Movie.objects.order_by('title', 'year', 'director__last_name', 'director__first_name')

    buffer = io.BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    workbook.remove_timezone = True

    workbook_properties = EXPORT_FILE_PROPERTIES.copy()
    workbook_properties['created'] = datetime.now()
    workbook.set_properties(workbook_properties)

    worksheet = workbook.add_worksheet('Movies')

    for col, field_titles in enumerate(MOVIES_EXPORT_FIELD_TITLES):
        worksheet.set_column(col, col, field_titles.width)

    date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})
    title_format = workbook.add_format({'bg_color': '#BEDFFA'})
    text_left__format = workbook.add_format({'align': 'left'})

    row = 0
    for col, field_titles in enumerate(MOVIES_EXPORT_FIELD_TITLES):
        worksheet.write(row, col, field_titles.name, title_format)

    row = 1
    for movie in movies:
        col_fields = _get_movies_export_field_values(movie, text_left__format, date_format)
        for col, col_field in enumerate(col_fields):
            worksheet.write(row, col, col_field['val'], col_field['format'])
        row += 1

    workbook.close()
    buffer.seek(0)
    log.info("Exporting movies report: Report ready to send.")

    return FileResponse(buffer, as_attachment=True, filename=MOVIES_EXPORT_FILE_NAME)


def export_movies_report(request):
    res, error_msg = None, None
    is_error = False
    try:
        res = _export_movies_report()
    except Exception as e:
        is_error = True
        error_msg = "Error exporting movies data"
        log.error("%s. Error msg: %s", error_msg, e)

    return (res or render(request, 'catalog/settings.html',
                          context={
                              'data': config_settings['settings'],
                              'is_error': is_error, 'error_msg': error_msg,
                            }))


def _fetch_external_movies_data(request):
    if not controller.client:
        controller.get_client()

    log_prefix = "Auto Fetch External Movies Data --- "
    movies = Movie.objects.filter(ext_title__exact=''). \
        order_by('title', 'director__last_name', 'director__first_name', 'year')

    movies_count = movies.count()
    processed_count = 0
    process_max = min(
        config_settings['settings'].auto_fetch_ext_resources_limit, movies_count)

    for movie in movies:
        processed_count +=1

        log.info(f"{log_prefix}Process {processed_count:3} of {process_max} movies")
        log.info(f"{log_prefix}Movie: {movie.title} [{movie.year}]")

        search_movie_title = movie.title
        search_movie_year = str(movie.year) or ''

        filter_ = f"include_adult=false"
        if search_movie_year:
            filter_ += f"&year={search_movie_year}"

        tmdb_data = controller.get_search_movie(search_movie_title, filter_)

        # if tmdb_data persist its fields to the db and save
        if tmdb_data:
            set_movie_external_data_fields(movie, tmdb_data[0])
        else:
            movie.ext_title = 'not_found'
            movie.save()

        if processed_count >= process_max:
            break
        time.sleep(config_settings['settings'].auto_fetch_ext_resources_sleep)

    log.info(f"{log_prefix}Movies candidates found to change: {movies_count}")
    log.info(f"{log_prefix}Processed movies: {processed_count} "
             f"of a max of {process_max}")


def fetch_external_movies_data(request):
    res, error_msg = None, None
    is_error = False
    try:
        _fetch_external_movies_data(request)
    except Exception as e:
        is_error = True
        error_msg = "Error fetching external movies data"
        log.error("%s. Error msg: %s", error_msg, e)

    return render(
        request, 'catalog/settings.html',
        context={
            'data': config_settings['settings'],
            'is_error': is_error, 'error_msg': error_msg,
            })
