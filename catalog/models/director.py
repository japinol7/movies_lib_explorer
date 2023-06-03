from django.db import models


class Director(models.Model):
    last_name = models.CharField(max_length=52)
    first_name = models.CharField(max_length=52, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    picture = models.ImageField(blank=True, null=True)

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
