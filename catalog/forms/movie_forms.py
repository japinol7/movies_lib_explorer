from django.forms import ModelForm, Textarea, TextInput

from catalog.models.movie import Movie


class MovieEditForm(ModelForm):
    class Meta:
        model = Movie
        exclude = ['picture', 'created', 'updated']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'title_original': TextInput(attrs={'class': 'form-control'}),
            'country': TextInput(attrs={'placeholder': "Ex: US", 'class': 'form-control'}),
            'language': TextInput(attrs={'placeholder': "Ex: English", 'class': 'form-control'}),
            'cast': Textarea(attrs={
                'cols': 76, 'rows': 4,
                'placeholder': "Ex: Errol Flynn, Olivia de Havilland",
                'class': 'form-control'}),
            'genres': TextInput(attrs={'class': 'form-control'}),
            'writer': TextInput(attrs={'class': 'form-control'}),
            'producer': TextInput(attrs={'class': 'form-control'}),
            'cinematography': TextInput(attrs={'class': 'form-control'}),
            'production_company': TextInput(attrs={'class': 'form-control'}),
            'note': Textarea(attrs={'cols': 70, 'rows': 2, 'class': 'form-control'}),
            'description': Textarea(attrs={'cols': 70, 'rows': 2, 'class': 'form-control'}),
            }
        labels = {
            'runtime': "Runtime in min.",
            'decade': "Decade [ex: 1950]",
            }
