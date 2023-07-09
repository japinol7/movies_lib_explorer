from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from catalog.config.config import MOVIE_YEAR_MIN, MOVIE_YEAR_MAX
from catalog.models.actor import Actor
from catalog.models.director import Director
from catalog.models.movie import Movie


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'first_name', 'last_name', 'created', 'updated']


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'first_name', 'last_name', 'created', 'updated']


class DirectorSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['first_name', 'last_name']


class MovieSerializer(serializers.ModelSerializer):
    director_data = DirectorSmallSerializer(source='director', read_only=True)
    actors = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'title_original', 'director', 'director_data', 'runtime',
            'year', 'country', 'language', 'cast', 'actors', 'genres',
            'writer', 'producer', 'cinematography', 'production_company', 'note',
            'description', 'created', 'updated',
            ]
        extra_kwargs = {
            'year': {
                'min_value': MOVIE_YEAR_MIN,
                'max_value': MOVIE_YEAR_MAX,
                },
            }
        validators = [
            UniqueTogetherValidator(
                queryset=Movie.objects.all(),
                fields=['title', 'year'],
                ),
            ]
