from collections import defaultdict
from itertools import groupby
from pathlib import Path
import time
import urllib

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404

from catalog.config.config import (
    MOVIE_GENRES,
    config_settings,
    TIME_SLEEP_WHEN_FEED_CONTENT,
    )
from catalog.models.actor import Actor
from catalog.models.director import Director
from catalog.models.movie import Movie
from catalog.forms.movie_forms import MovieEditForm
from catalog.src_modules.controller.tmdb_controller import TMDBController, TMDB_CONNECTOR_INFO
from tools.logger.logger import log

controller = TMDBController()


def movie_list(request):
    data = {
        'movies': Movie.objects.select_related('director').
                  order_by(
                    'title', 'year', 'director__last_name', 'director__first_name', 'year'
                  )[:config_settings['settings'].movies_list_limit],
        'default_movies_list_limit': config_settings['settings'].movies_list_limit,
        }
    return render(request, "catalog/movie_list.html", data)


def movie_with_picture_list(request):
    movies = Movie.objects.all().exclude(picture='')
    paginator = Paginator(movies, 2)
    page_num = int(request.GET.get("page", 1))

    if page_num < 1:
        page_num = 1
    elif page_num > paginator.num_pages:
        page_num = paginator.num_pages

    page = paginator.page(page_num)

    data = {
        "movies": page.object_list,
        "more_movies": page.has_next(),
        "next_page": page_num + 1,
        }

    if request.htmx:
        if TIME_SLEEP_WHEN_FEED_CONTENT > 0:
            time.sleep(TIME_SLEEP_WHEN_FEED_CONTENT)
        return render(request, "catalog/partials/movie_with_picture_list_results.html", data)

    return render(request, "catalog/movie_with_picture_list.html", data)


def movie_list_by_year(request):
    data = {
        'movies': Movie.objects.select_related('director').
                  order_by(
                    'year', 'title', 'director__last_name', 'director__first_name'
                  )[:config_settings['settings'].movies_list_limit],
        'default_movies_list_limit': config_settings['settings'].movies_list_limit,
        }
    data.update(_group_data_by_year(data['movies']))
    return render(request, "catalog/movie_list_by_year.html", context=data)


def _group_data_by_year(data):
    def key_func(x):
        return x[0]

    data_with_year = ((x.year, x) for x in data)
    data_by_year = groupby(sorted(data_with_year, key=key_func), key_func)

    res = defaultdict(list)
    for year, movies in data_by_year:
        for movie in movies:
            res[year].append(movie)

    return {
        'years': dict(res)
        }


def movie_list_by_decade(request):
    data = {
        'movies': Movie.objects.select_related('director').
                  order_by(
                    'year', 'title', 'director__last_name', 'director__first_name'
                  )[:config_settings['settings'].movies_list_limit],
        'default_movies_list_limit': config_settings['settings'].movies_list_limit,
    }
    data.update(_group_data_by_decade(data['movies']))
    return render(request, "catalog/movie_list_by_decade.html", context=data)


def _group_data_by_decade(data):
    def key_func(x):
        return x[0]

    data_with_decade = ((x.decade, x) for x in data)
    data_by_decade = groupby(sorted(data_with_decade, key=key_func), key_func)

    res = defaultdict(list)
    for decade, movies in data_by_decade:
        for movie in movies:
            res[decade].append(movie)

    return {
        'decades': dict(res)
        }


def movie_list_by_genre(request):
    data = {'movies': []}
    search_genre = ''
    if request.method == 'POST':
        search_genre = request.POST.get('search_genres') or ''
        if search_genre:
            data['movies'] = list(
                Movie.objects.filter(genres__contains=search_genre).select_related('director').
                order_by(
                    'title', 'year', 'director__last_name', 'director__first_name'
                )[:config_settings['settings'].movies_list_limit]
                )

    return render(request, "catalog/movie_list_by_genre.html",
                  context={
                      'movies': data['movies'],
                      'genres': MOVIE_GENRES,
                      'search_genre': search_genre,
                      'default_movies_list_limit': config_settings['settings'].movies_list_limit,
                  })


def movie_list_search(request):
    search_text = request.GET.get('search_text', '')
    search_text = urllib.parse.unquote(search_text)
    search_text = search_text.strip()

    movies = []
    if search_text:
        parts = search_text.split()
        q = (Q(title__icontains=parts[0]) | Q(director__last_name__icontains=parts[0])
             | Q(director__first_name__icontains=parts[0]))
        for part in parts[1:]:
            q |= (Q(title__icontains=part) | Q(director__last_name__icontains=part)
                  | Q(director__first_name__icontains=parts[0]))
        movies = Movie.objects.filter(q)[:config_settings['settings'].movies_list_limit]

    data = {
        "search_text": search_text,
        "movies": movies,
        'default_movies_list_limit': config_settings['settings'].movies_list_limit,
        }
    if request.htmx:
        return render(request, "catalog/partials/movie_list_search_results.html",
                      context=data)
    return render(request, "catalog/movie_list_search.html",
                  context=data)


def movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    actors = Actor.objects.filter(movie=movie)
    return render(request, 'catalog/movie.html',
                  {'movie': movie, 'actors': actors})


@login_required
def upload_movie_photo(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    data = {
        'movie': movie,
        }
    if request.method == 'GET':
        return render(request, 'catalog/upload_movie_photo.html', data)

    # POST
    upload = request.FILES['movie_photo']
    # TODO: Do not use the file name as given by the user as part of the file name,
    #  it could contain characters than could cause problems.
    path = Path(settings.MEDIA_ROOT) / f'{request.user.id}_movie_{upload.name}'
    with open(path, 'wb+') as output:
        for chunk in upload.chunks():
            output.write(chunk)
    movie.picture = path.name
    movie.save()
    return redirect('catalog:movie', movie.id)


@login_required
def movie_create_form(request):
    log.info("Start view: movie_create_form")

    data = {
        'directors': Director.objects.all().order_by('last_name', 'first_name'),
        }

    if request.method == 'POST':
        if not request.user.is_staff:
            raise PermissionDenied("Permission Denied. You are not allowed to create a document for this model")
        movie_title = request.POST.get('movie_title', '').strip()
        movie_year = request.POST.get('movie_year')
        movie_director_id = request.POST.get('movie_director_id')
        if movie_title and movie_year and movie_director_id:
            movie = Movie.objects.create(
                title=movie_title,
                title_original=movie_title,
                director_id=movie_director_id,
                year=movie_year)
            movie.save()
            log.info(f"Movie created: {movie}")
            return redirect('catalog:movie', movie.id)

    return render(request, 'catalog/movie_create_form.html',
                  context=data)


@login_required
def movie_edit_form(request, movie_id):
    log.info(f"Start view: movie_edit_form - movie_id: {movie_id}")
    movie = get_object_or_404(Movie, id=movie_id)
    form = MovieEditForm(instance=movie)

    if request.method == 'POST':
        if not request.user.is_staff:
            raise PermissionDenied("Permission Denied. You are not allowed to edit this model")
        form = MovieEditForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('catalog:movie', movie.id)

    return render(request, 'catalog/movie_edit_form.html',
                  {'movie': movie, 'form': form})


@login_required
def movie_delete_form(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST':
        if not request.user.is_staff:
            raise PermissionDenied("Permission Denied. You are not allowed to delete a document for this model")
        log.info(f"Delete movie : {movie}")
        movie.delete()
        return redirect('catalog:movie_list')

    return render(request, 'catalog/movie_delete_form.html',
                  {'movie': movie})


@login_required
def tmdb_movie_link(request, movie_id):
    log.info(f"Start view: tmdb_movie_link - movie_id: {movie_id}")
    movie = get_object_or_404(Movie, id=movie_id)

    return render(request, 'catalog/partials/tmdb_movie_link.html',
                  context={'movie': movie})


@login_required
def tmdb_movie_search_form(request, movie_id):
    log.info(f"Start view: tmdb_movie_search_form - movie_id: {movie_id}")
    movie = get_object_or_404(Movie, id=movie_id)

    tmdb_data = []
    if request.method == 'POST':
        search_movie_title = request.POST.get('search_movie_title')
        search_movie_year = request.POST.get('search_movie_year') or ''

        filter_ = f"include_adult=false"
        if search_movie_year:
            filter_ += f"&year={search_movie_year}"

        if not controller.client:
            controller.get_client()

        tmdb_data = controller.get_search_movie(search_movie_title, filter_)

    return render(request, 'catalog/partials/tmdb_movie_search_form.html',
                  context={
                      'movie': movie,
                      'tmdb_movies': tmdb_data,
                      'tmdb_info': TMDB_CONNECTOR_INFO,
                      'tmdb_errors': controller.tmdb_errors,
                  })
