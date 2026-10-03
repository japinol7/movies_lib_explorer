from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from catalog.config.config import (
    DEFAULT_AUTO_FETCH_EXT_RESOURCES_LIMIT,
    DEFAULT_MOVIES_LIST_LIMIT,
    DEFAULT_PEOPLE_LIST_LIMIT,
    MAX_MOVIES_LIST_LIMIT,
    MAX_PEOPLE_LIST_LIMIT,
    MAX_AUTO_FETCH_EXT_RESOURCES_LIMIT,
    DEFAULT_AUTO_FETCH_EXT_RESOURCES_SLEEP,
    MIN_AUTO_FETCH_EXT_RESOURCES_SLEEP,
    MAX_AUTO_FETCH_EXT_RESOURCES_SLEEP,
    )


class Settings(models.Model):
    movies_list_limit = models.IntegerField(
        default=DEFAULT_MOVIES_LIST_LIMIT,
        validators=[MinValueValidator(1), MaxValueValidator(MAX_MOVIES_LIST_LIMIT)]
        )
    people_list_limit = models.IntegerField(
        default=DEFAULT_PEOPLE_LIST_LIMIT,
        validators=[MinValueValidator(1), MaxValueValidator(MAX_PEOPLE_LIST_LIMIT)]
        )
    auto_fetch_ext_resources_limit = models.IntegerField(
        default=DEFAULT_AUTO_FETCH_EXT_RESOURCES_LIMIT,
        validators=[
            MinValueValidator(1), MaxValueValidator(MAX_AUTO_FETCH_EXT_RESOURCES_LIMIT)]
        )
    auto_fetch_ext_resources_sleep = models.IntegerField(
        default=DEFAULT_AUTO_FETCH_EXT_RESOURCES_SLEEP,
        validators=[
            MinValueValidator(MIN_AUTO_FETCH_EXT_RESOURCES_SLEEP),
            MaxValueValidator(MAX_AUTO_FETCH_EXT_RESOURCES_SLEEP)]
        )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Settings'
        verbose_name_plural = 'Settings'

    def __str__(self):
        return f"movies_list_limit: {self.movies_list_limit}" \
               f"people_list_limit: {self.people_list_limit}"

    def __repr__(self):
        return f'Settings(id={self.id}, ' \
               f'movies_list_limit="{self.movies_list_limit}", ' \
               f'people_list_limit="{self.people_list_limit}")'
