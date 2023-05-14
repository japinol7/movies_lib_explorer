from django.test import TestCase


class HomeTestCase(TestCase):
    def test_home(self):
        response = self.client.get('/home/sample/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("movies", response.context)

        response = self.client.get('/home/about/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
