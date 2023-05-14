from django.test import TestCase
from rest_framework import status


class HomeTestCase(TestCase):
    def test_home(self):
        response = self.client.get('/home/sample/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("movies", response.context)

        response = self.client.get('/home/about/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
