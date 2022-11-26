from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from catalog.models.director import Director
from catalog.models.movie import Movie
from review.models.review import Review


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
        movie_url = reverse('movie', args=(movie.id,))
        response = self.client.get(movie_url)
        self.assertEqual(200, response.status_code)
        self.assertIn("No reviews yet!", str(response.content))

        # Verify login redirect
        review_url = reverse('review_movie', args=(movie.id,))
        response = self.client.get(review_url)
        self.assertEqual(302, response.status_code)
        self.assertIn('login', response.url)

        # Post a review
        review_data1 = {
            'rating': 1,
            'text': 'This is some review text',
            }
        self.client.login(username=self.users[0], password=self.PASSWORD)
        response = self.client.post(review_url, review_data1)
        self.assertEqual(302, response.status_code)
        self.assertEqual(f'/catalog/movie/{movie.id}/', response.url)

        review = movie.review_set.first()
        self.assertEqual(review_data1['rating'], review.rating)
        self.assertEqual(review_data1['text'], review.text)

        # Post another review
        review_data2 = {
            'rating': 2,
            'text': 'More review text',
            }

        self.client.login(username=self.users[1], password=self.PASSWORD)
        self.client.post(review_url, review_data2)

        review = movie.review_set.all()[1]
        self.assertEqual(review_data2['rating'], review.rating)
        self.assertEqual(review_data2['text'], review.text)

        # Verify that the movie page has reviews
        self.client.logout()
        response = self.client.get(movie_url)
        self.assertEqual(200, response.status_code)
        self.assertIn(f"{self.users[0].username} rating {review_data1['rating']}",
                      str(response.content))
        self.assertIn(f"{self.users[1].username} rating {review_data2['rating']}",
                      str(response.content))

        # Verify there are only two reviews
        num = str(response.content).count("card-body")
        self.assertEqual(2, num)
