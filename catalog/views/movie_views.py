from collections import defaultdict
from itertools import groupby
from pathlib import Path

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render, get_object_or_404

from catalog.models.actor import Actor
from catalog.models.movie import Movie
from catalog.forms.movie_forms import MovieEditForm


def movie_list(request):
    data = {
        'movies': Movie.objects.select_related('director').
                  order_by('title', 'year', 'director__last_name', 'director__first_name', 'year')
        }
    return render(request, "catalog/movie_list.html", data)


def movie_with_picture_list(request):
    data = {
        'movies': Movie.objects.exclude(picture='').select_related('director').
                  order_by('title', 'director__last_name', 'director__first_name', 'year')
        }
    return render(request, "catalog/movie_with_picture_list.html", data)


def movie_list_by_year(request):
    data = {
        'movies': Movie.objects.select_related('director').
                  order_by('year', 'title', 'director__last_name', 'director__first_name')
        }
    return render(request, "catalog/movie_list_by_year.html", _group_data_by_year(data['movies']))


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
                  order_by('title', 'year', 'director__last_name', 'director__first_name')
        }
    return render(request, "catalog/movie_list_by_decade.html", _group_data_by_decade(data['movies']))


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
def movie_edit_form(request, movie_id):
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
