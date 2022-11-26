from django.shortcuts import render

from catalog.models.movie import Movie
from catalog.models.director import Director
from tools.logger.logger import  log
from tools.utils.import_data import import_if_empty


def load_data(request):
    # TODO: Import movies and directors form csv files
    data = {
        'movies': Movie.objects.order_by('title', 'director__last_name', 'director__first_name', 'year'),
        'directors': Director.objects.order_by('last_name', 'first_name'),
        }
    if data['movies'] or data['directors']:
        log.info("Skip import data. There is already data in the dabatase.")
        return render(request, 'catalog/load_data_aborted.html', data)

    import_if_empty()

    data = {
        'movies': Movie.objects.order_by('title', 'director__last_name', 'director__first_name', 'year')
        }
    return render(request, 'catalog/load_data.html', data)
