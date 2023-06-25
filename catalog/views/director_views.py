from pathlib import Path

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render, get_object_or_404

from catalog.models.director import Director
from catalog.forms.director_forms import DirectorEditForm


def director_list(request):
    data = {
        'directors': Director.objects.order_by('last_name', 'first_name'),
        }
    return render(request, 'catalog/director_list.html', data)


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
