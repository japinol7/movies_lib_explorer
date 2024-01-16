from django.forms import ModelForm, NumberInput

from catalog.models.settings import Settings


class SettingsEditForm(ModelForm):
    class Meta:
        model = Settings
        exclude = ['created', 'updated']
        widgets = {
            'movies_list_limit': NumberInput(attrs={'class': 'form-control'}),
            'people_list_limit': NumberInput(attrs={'class': 'form-control'}),
            }
        labels = {
            'movies_list_limit': "Movies list limit",
            'people_list_limit': "People list limit",
            }
