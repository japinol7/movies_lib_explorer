from django.db import models

from catalog.models.actor import Actor
from catalog.models.director import Director


class Movie(models.Model):
    title = models.CharField(max_length=90)
    title_original = models.CharField(max_length=90)
    director = models.ForeignKey(
        Director, on_delete=models.DO_NOTHING,
        blank=True, null=True,
        )
    actors = models.ManyToManyField(
        Actor,
        blank=True,
        )
    runtime = models.IntegerField(default=0)
    year = models.IntegerField(default=0)
    decade = models.IntegerField(default=0)
    country = models.CharField(max_length=3, blank=True)
    language = models.CharField(max_length=25, blank=True)
    cast = models.CharField(max_length=400, blank=True)
    genres = models.CharField(max_length=254, blank=True)
    writer = models.CharField(max_length=60, blank=True)
    producer = models.CharField(max_length=60, blank=True)
    cinematography = models.CharField(max_length=60, blank=True)
    production_company = models.CharField(max_length=90, blank=True)
    note = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=900, blank=True)
    picture = models.ImageField(blank=True, null=True)

    class Meta:
        ordering = ['title', 'director__last_name', 'director__first_name']
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'
        indexes = [
            models.Index(fields=['title', 'director']),
            models.Index(fields=['year', 'title', 'director']),
            models.Index(fields=['decade', 'year', 'title', 'director']),
            ]

    def __str__(self):
        return f"Id: {self.id}, \n" \
               f"Title: {self.title}, \n" \
               f"Year: {self.year}, \n" \
               f"Director: {self.director}"

    def __repr__(self):
        return f'Movie(id={self.id}, title="{self.title}", director_id={self.director.id})'
