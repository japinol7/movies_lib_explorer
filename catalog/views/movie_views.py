from pathlib import Path

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from catalog.models.actor import Actor
from catalog.models.movie import Movie


def movie_list(request):
    data = {
        'movies': Movie.objects.order_by('title', 'director__last_name', 'director__first_name', 'year')
        }
    return render(request, "catalog/movie_list.html", data)


def movie_with_picture_list(request):
    data = {
        'movies': Movie.objects.exclude(picture='').order_by(
            'title', 'director__last_name', 'director__first_name', 'year')
        }
    return render(request, "catalog/movie_with_picture_list.html", data)


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
    return redirect('movie', movie.id)
