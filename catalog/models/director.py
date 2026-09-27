from django.db import models


class Director(models.Model):
    last_name = models.CharField(max_length=52)
    first_name = models.CharField(max_length=52, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    picture = models.ImageField(blank=True, null=True)

    # External fetched fields
    ext_name = models.CharField(max_length=110, blank=True)
    ext_birth_date = models.CharField(max_length=50, blank=True)
    ext_death_date = models.CharField(max_length=50, blank=True)
    ext_birth_place = models.CharField(max_length=254, blank=True)
    ext_biography = models.CharField(max_length=8000, blank=True)
    ext_picture_uri = models.CharField(max_length=1024, blank=True)
    ext_picture = models.ImageField(blank=True, null=True)
    ext_tmdb_id = models.CharField(max_length=110, blank=True)
    ext_imdb_id = models.CharField(max_length=110, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Director'
        verbose_name_plural = 'Directors'
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
            ]

    def __str__(self):
        return f"{self.first_name}{self.first_name and ' ' or ''}" \
               f"{self.last_name} [{self.id}]"

    def __repr__(self):
        return f'Director(id={self.id}, ' \
               f'first_name="{self.first_name}", ' \
               f'last_name="{self.last_name}")'
