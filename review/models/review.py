from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from catalog.models.movie import Movie


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1), MaxValueValidator(5)))
    text = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'movie'], name="unique_review"),
            ]

    def __str__(self):
        return f"Review(id={self.id}, user={self.user.username}, movie={self.movie.title})"
