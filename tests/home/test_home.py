from django.test import TestCase


class HomeTestCase(TestCase):
    def test_home(self):
        response = self.client.get('/home/sample/')
        self.assertEqual(200, response.status_code)
        self.assertIn("movies", response.context)

        response = self.client.get('/home/about/')
        self.assertEqual(200, response.status_code)

        response = self.client.get('/')
        self.assertEqual(200, response.status_code)
