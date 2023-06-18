from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from catalog.models.director import Director
from catalog.models.movie import Movie


class ReviewTestCase(TestCase):
    PASSWORD = 'asdfasdf33'

    def setUp(self):
        super().setUp()
        self.users = []

        for x in range(3):
            user = User.objects.create_user(f'user{x}', f'user{x}@example.com', self.PASSWORD)
            self.users.append(user)

    def test_reviews(self):
        director = Director.objects.create(
            last_name="director_last_name",
            first_name="director_first_name")
        movie = Movie.objects.create(title="movie", director=director, year=1900)

        # Verify no-review state
        movie_url = reverse('catalog:movie', args=(movie.id,))
        response = self.client.get(movie_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("No reviews yet!", str(response.content))

        # Verify login redirect
        review_url = reverse('review:review_movie', args=(movie.id,))
        response = self.client.get(review_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

        # Post a review
        review_data1 = {
            'rating': 1,
            'text': 'This is some review text',
            }
        self.client.login(username=self.users[0], password=self.PASSWORD)
        response = self.client.post(review_url, review_data1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/catalog/movie/{movie.id}/')

        review = movie.review_set.first()
        self.assertEqual(review.rating, review_data1['rating'])
        self.assertEqual(review.text, review_data1['text'])

        # Post another review
        review_data2 = {
            'rating': 2,
            'text': 'More review text',
            }

        self.client.login(username=self.users[1], password=self.PASSWORD)
        self.client.post(review_url, review_data2)

        review = movie.review_set.all()[1]
        self.assertEqual(review.rating, review_data2['rating'])
        self.assertEqual(review.text, review_data2['text'])

        # Verify that the movie page has reviews
        self.client.logout()
        response = self.client.get(movie_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(f"{self.users[0].username} rating {review_data1['rating']}",
                      str(response.content))
        self.assertIn(f"{self.users[1].username} rating {review_data2['rating']}",
                      str(response.content))

        # Verify there are only two reviews
        num = str(response.content).count("card-body")
        self.assertEqual(num, 2)
