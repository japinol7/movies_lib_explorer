from pathlib import Path

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render, get_object_or_404

from catalog.import_data.import_data import (
    update_actors_n_movie_actor_links,
    get_data_to_update_actors_n_movie_actor_links,
    )
from catalog.models.actor import Actor
from catalog.forms.actor_forms import ActorEditForm
from tools.logger.logger import log


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
