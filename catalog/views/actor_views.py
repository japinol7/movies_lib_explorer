import time
import urllib

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404

from catalog.config.config import (
    config_settings,
    TIME_SLEEP_WHEN_FEED_CONTENT,
    )
from catalog.src_modules.import_data.import_data import (
    update_actors_n_movie_actor_links,
    get_data_to_update_actors_n_movie_actor_links,
    )
from catalog.models.actor import Actor
from catalog.forms.actor_forms import ActorEditForm
from catalog.services.actor_services import set_actor_external_data_fields
from catalog.services.resource_services import (
    get_person_full_name,
    save_uploaded_picture_to_resource,
    )
from catalog.src_modules.controller.tmdb_controller import (
    TMDBController,
    TMDB_CONNECTOR_INFO,
    )
from tools.logger.logger import log

controller = TMDBController()


def actor_list(request):
    data = {
        'actors': [],
        }
    return render(request, 'catalog/actor_list.html', context=data)


def actor_list_search(request):
    search_text = request.GET.get('search_text', '')
    search_text = urllib.parse.unquote(search_text)
    search_text = search_text.strip()

    actors = []
    if search_text:
        parts = search_text.split()
        q = (Q(last_name__icontains=parts[0]) | Q(first_name__icontains=parts[0]))
        for part in parts[1:]:
            q |= (Q(last_name__icontains=part) | Q(first_name__icontains=parts[0]))
        actors = Actor.objects.filter(q)[:config_settings['settings'].people_list_limit]

    data = {
        "search_text": search_text,
        "actors": actors,
        'default_people_list_limit': config_settings['settings'].people_list_limit,
        }
    if request.htmx:
        return render(request, "catalog/partials/actor_list_search_results.html",
                      context=data)
    return render(request, "catalog/actor_list.html",
                  context=data)


def actor_with_picture_list(request):
    actors = Actor.objects.all().exclude(picture='')
    paginator = Paginator(actors, 2)
    page_num = int(request.GET.get("page", 1))

    if page_num < 1:
        page_num = 1
    elif page_num > paginator.num_pages:
        page_num = paginator.num_pages

    page = paginator.page(page_num)

    data = {
        "actors": page.object_list,
        "more_actors": page.has_next(),
        "next_page": page_num + 1,
        }

    if request.htmx:
        if TIME_SLEEP_WHEN_FEED_CONTENT > 0:
            time.sleep(TIME_SLEEP_WHEN_FEED_CONTENT)
        return render(
            request, "catalog/partials/actor_with_picture_list_results.html", data)

    return render(request, "catalog/actor_with_picture_list.html", data)


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
    actor_name = get_person_full_name(actor.first_name, actor.last_name)
    uploaded_file = request.FILES['actor_photo']
    save_uploaded_picture_to_resource(actor, uploaded_file, actor_name)

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

        # if tmdb_data persist its fields to the db and save
        if tmdb_data:
            set_actor_external_data_fields(actor, tmdb_data[0])

    return render(request, 'catalog/partials/tmdb_actor_search_form.html',
                  context={
                      'actor': actor,
                      'tmdb_actors': tmdb_data,
                      'tmdb_info': TMDB_CONNECTOR_INFO,
                      'tmdb_errors': controller.tmdb_errors,
                  })
