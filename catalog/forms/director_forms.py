from django.forms import ModelForm, TextInput

from catalog.models.director import Director


class DirectorEditForm(ModelForm):
    class Meta:
        model = Director
        fields = ['first_name', 'last_name']
        widgets = {
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            }
