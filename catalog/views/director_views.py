from pathlib import Path
import urllib

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404

from catalog.config.config import config_settings
from catalog.models.director import Director
from catalog.forms.director_forms import DirectorEditForm
from catalog.src_modules.controller.tmdb_controller import TMDBController, TMDB_CONNECTOR_INFO
from tools.logger.logger import log

controller = TMDBController()


def director_list(request):
    data = {
        'directors': [],
        }
    return render(request, 'catalog/director_list.html', context=data)


def director_list_search(request):
    search_text = request.GET.get('search_text', '')
    search_text = urllib.parse.unquote(search_text)
    search_text = search_text.strip()

    directors = []
    if search_text:
        parts = search_text.split()
        q = (Q(last_name__icontains=parts[0]) | Q(first_name__icontains=parts[0]))
        for part in parts[1:]:
            q |= (Q(last_name__icontains=part) | Q(first_name__icontains=parts[0]))
        directors = Director.objects.filter(q)[:config_settings['settings'].people_list_limit]

    data = {
        "search_text": search_text,
        "directors": directors,
        'default_people_list_limit': config_settings['settings'].people_list_limit,
        }
    if request.htmx:
        return render(request, "catalog/partials/director_list_search_results.html",
                      context=data)
    return render(request, "catalog/director_list.html",
                  context=data)


def director(request, director_id):
    director = get_object_or_404(Director, id=director_id)
    return render(request, 'catalog/director.html', {'director': director})


@login_required
def upload_director_photo(request, director_id):
    director = get_object_or_404(Director, id=director_id)
    data = {
        'director': director,
        }
    if request.method == 'GET':
        return render(request, 'catalog/upload_director_photo.html', data)

    # POST
    upload = request.FILES['director_photo']
    # TODO: Do not use the file name as given by the user as part of the file name,
    #  it could contain characters than could cause problems.
    path = Path(settings.MEDIA_ROOT) / f'{request.user.id}_director_{upload.name}'
    with open(path, 'wb+') as output:
        for chunk in upload.chunks():
            output.write(chunk)
    director.picture = path.name
    director.save()
    return redirect('catalog:director', director.id)


@login_required
def director_edit_form(request, director_id):
    director = get_object_or_404(Director, id=director_id)
    form = DirectorEditForm(instance=director)

    if request.method == 'POST':
        if not request.user.is_staff:
            raise PermissionDenied("Permission Denied. You are not allowed to edit this model")
        form = DirectorEditForm(request.POST, instance=director)
        if form.is_valid():
            form.save()
            return redirect('catalog:director', director.id)

    return render(request, 'catalog/director_edit_form.html',
                  {'director': director, 'form': form})


@login_required
def tmdb_director_link(request, director_id):
    log.info(f"Start view: tmdb_director_link - director_id: {director_id}")
    director = get_object_or_404(Director, id=director_id)

    return render(request, 'catalog/partials/tmdb_director_link.html',
                  context={'director': director})


@login_required
def tmdb_director_search_form(request, director_id):
    log.info(f"Start view: tmdb_director_search_form - director_id: {director_id}")
    director = get_object_or_404(Director, id=director_id)

    tmdb_data = []
    if request.method == 'POST':
        search_director_name = request.POST.get('search_director_name')

        if not controller.client:
            controller.get_client()

        tmdb_data = controller.get_search_person(search_director_name, filter_='')

    return render(request, 'catalog/partials/tmdb_director_search_form.html',
                  context={
                      'director': director,
                      'tmdb_directors': tmdb_data,
                      'tmdb_info': TMDB_CONNECTOR_INFO,
                      'tmdb_errors': controller.tmdb_errors,
                  })
