from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect

from catalog.config.config import config_settings, update_config_settings
from catalog.forms.settings_forms import SettingsEditForm
from catalog.models.settings import Settings


def catalog_settings(request):
    return render(
        request, 'catalog/settings.html',
        context={
            'data': config_settings['settings'],
            }
        )


@login_required
def settings_edit_form(request, settings_id):
    settings = get_object_or_404(Settings, id=settings_id)
    form = SettingsEditForm(instance=settings)

    if request.method == 'POST':
        if not request.user.is_staff:
            raise PermissionDenied("Permission Denied. You are not allowed to edit this model")
        form = SettingsEditForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            update_config_settings(Settings)
            return redirect('catalog:settings')

    return render(request, 'catalog/settings_edit_form.html',
                  {'settings': settings, 'form': form})
