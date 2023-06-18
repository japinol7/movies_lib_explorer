from django.urls import reverse
from django.test import TestCase

from catalog.models.director import Director
from catalog.models.movie import Movie


class CatalogTestCase(TestCase):

    def setUp(self):
        super().setUp()
        director = Director.objects.create(last_name="Kurusawa")
        Movie.objects.create(title="Seven samurais", director=director, year=1954)

    def test_movie_director_repr(self):
        movie = Movie.objects.get(id=1)
        result = repr(movie)
        expected = f'director_id={movie.director.id}'
        self.assertIn(expected, result)

    def test_movie_repr(self):
        movie = Movie.objects.get(id=1)
        result = repr(movie)
        expected = f'title="{movie.title}"'
        self.assertIn(expected, result)

    def test_movie_list(self):
        response = self.client.get(
            path=reverse('catalog:movie_list'),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["movies"]), 1)
