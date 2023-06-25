from django.forms import ModelForm, TextInput

from catalog.models.director import Director


class DirectorEditForm(ModelForm):
    class Meta:
        model = Director
        fields = ['last_name', 'first_name']
        widgets = {
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            }
