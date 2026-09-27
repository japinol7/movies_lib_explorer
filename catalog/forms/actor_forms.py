from django.forms import ModelForm, TextInput

from catalog.models.actor import Actor


class ActorEditForm(ModelForm):
    class Meta:
        model = Actor
        exclude = ['picture', 'created', 'updated']
        widgets = {
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            }
