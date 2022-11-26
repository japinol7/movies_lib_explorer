from django.db import models


class Director(models.Model):
    last_name = models.CharField(max_length=52)
    first_name = models.CharField(max_length=52, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    picture = models.ImageField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} [{self.id}]"

    def __repr__(self):
        return f'Director(id={self.id}, ' \
               f'first_name="{self.first_name}", ' \
               f'last_name="{self.last_name}")'
