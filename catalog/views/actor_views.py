from pathlib import Path

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render, get_object_or_404

from catalog.src_modules.import_data.import_data import (
    update_actors_n_movie_actor_links,
    get_data_to_update_actors_n_movie_actor_links,
    )
from catalog.models.actor import Actor
from catalog.forms.actor_forms import ActorEditForm
from catalog.src_modules.controller.tmdb_controller import TMDBController, TMDB_CONNECTOR_INFO
from tools.logger.logger import log

controller = TMDBController()


def actor_list(request):
    data = {
        'actors': Actor.objects.order_by('last_name', 'first_name'),
        }
    return render(request, 'catalog/actor_list.html', data)


def actor(request, actor_id):
    actor = get_object_or_404(Actor, id=actor_id)
    return render(request, 'catalog/actor.html', {'actor': actor})


def calc_new_actors_from_cast(request):
    data = get_data_to_update_actors_n_movie_actor_links()
    if not data['movies']:
        log.info("Skip calculating new actors from cast. There is no new data to process.")
        return render(request, 'catalog/calc_new_actors_from_cast_aborted.html', data)

    update_actors_n_movie_actor_links(data)

    data = {
        }
    return render(request, 'catalog/calc_new_actors_from_cast.html', data)


@login_required
def upload_actor_photo(request, actor_id):
    actor = get_object_or_404(Actor, id=actor_id)
    data = {
        'actor': actor,
        }
    if request.method == 'GET':
        return render(request, 'catalog/upload_actor_photo.html', data)

    # POST
    upload = request.FILES['actor_photo']
    # TODO: Do not use the file name as given by the user as part of the file name,
    #  it could contain characters than could cause problems.
    path = Path(settings.MEDIA_ROOT) / f'{request.user.id}_actor_{upload.name}'
    with open(path, 'wb+') as output:
        for chunk in upload.chunks():
            output.write(chunk)
    actor.picture = path.name
    actor.save()
    return redirect('catalog:actor', actor.id)


@login_required
def actor_edit_form(request, actor_id):
    actor = get_object_or_404(Actor, id=actor_id)
    form = ActorEditForm(instance=actor)

    if request.method == 'POST':
        if not request.user.is_staff:
            raise PermissionDenied("Permission Denied. You are not allowed to edit this model")
        form = ActorEditForm(request.POST, instance=actor)
        if form.is_valid():
            form.save()
            return redirect('catalog:actor', actor.id)

    return render(request, 'catalog/actor_edit_form.html',
                  {'actor': actor, 'form': form})


@login_required
def tmdb_actor_link(request, actor_id):
    log.info(f"Start view: tmdb_actor_link - actor_id: {actor_id}")
    actor = get_object_or_404(Actor, id=actor_id)

    return render(request, 'catalog/partials/tmdb_actor_link.html',
                  context={'actor': actor})


@login_required
def tmdb_actor_search_form(request, actor_id):
    log.info(f"Start view: tmdb_actor_search_form - actor_id: {actor_id}")
    actor = get_object_or_404(Actor, id=actor_id)

    tmdb_data = []
    if request.method == 'POST':
        search_actor_name = request.POST.get('search_actor_name')

        if not controller.client:
            controller.get_client()

        tmdb_data = controller.get_search_person(search_actor_name, filter_='')

    return render(request, 'catalog/partials/tmdb_actor_search_form.html',
                  context={
                      'actor': actor,
                      'tmdb_actors': tmdb_data,
                      'tmdb_info': TMDB_CONNECTOR_INFO,
                      'tmdb_errors': controller.tmdb_errors,
                  })
