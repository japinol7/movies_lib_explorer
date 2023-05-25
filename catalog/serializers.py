from rest_framework import serializers

from catalog.models.director import Director
from catalog.models.movie import Movie


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'first_name', 'last_name', 'created', 'updated']


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'title_original', 'director', 'runtime',
                  'year', 'country', 'language', 'cast', 'genres',
                  'writer', 'producer', 'cinematography', 'production_company', 'note',
                  'description', 'created', 'updated',
                  ]
