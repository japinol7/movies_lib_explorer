from pathlib import Path

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from catalog.models.actor import Actor


def actor_list(request):
    data = {
        'actors': Actor.objects.order_by('last_name', 'first_name'),
        }
    return render(request, 'catalog/actor_list.html', data)


def actor(request, actor_id):
    actor = get_object_or_404(Actor, id=actor_id)
    return render(request, 'catalog/actor.html', {'actor': actor})


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
    return redirect('actor', actor.id)
