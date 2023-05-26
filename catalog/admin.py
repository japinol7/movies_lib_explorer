from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from django.urls import reverse

from catalog.models.actor import Actor
from catalog.models.director import Director
from catalog.models.movie import Movie


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'show_movies')

    def show_movies(self, obj):
        count = Movie.objects.filter(
            models.Q(actors__first_name=obj.first_name) &
            models.Q(actors__last_name=obj.last_name)).count()

        url = reverse('admin:catalog_movie_changelist') + f'?actor__id={obj.id}'
        plural = 's' if count != 1 else ''
        return format_html('<a href="{}">{} Movie{}</a>', url, count, plural)


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'show_movies')

    def show_movies(self, obj):
        count = Movie.objects.filter(director=obj).count()
        url = reverse('admin:catalog_movie_changelist') + f'?director__id={obj.id}'
        plural = 's' if count != 1 else ''
        return format_html('<a href="{}">{} Movie{}</a>', url, count, plural)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'year', 'director_last_name')
    list_filter = ('director', )

    def director_last_name(self, obj):
        return obj.director.last_name
