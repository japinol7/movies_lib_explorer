import io
from datetime import datetime

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
    MOVIES_EXPORT_FIELD_NORMAL_WIDTH,
    EXPORT_FILE_PROPERTIES,
    )
from catalog.forms.settings_forms import SettingsEditForm
from catalog.models.movie import Movie
from catalog.models.settings import Settings


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
        {'val': movie.picture.name, 'format': text_left__format},
        {'val': movie.producer, 'format': text_left__format},
        {'val': movie.writer, 'format': text_left__format},
        {'val': movie.created, 'format': date_format},
        {'val': movie.updated, 'format': date_format},
    ]


def export_movies_report(request):
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

    return FileResponse(buffer, as_attachment=True, filename=MOVIES_EXPORT_FILE_NAME)
