from django.contrib.auth.models import User
from rest_framework import status
from django.test import TestCase


class UsersTestCase(TestCase):
    def test_userprofile_signal(self):
        user = User.objects.create(username="user_test", password="test_pwd_01")
        self.assertIsNotNone(user.userprofile)

    def test_404(self):
        response = self.client.get('/not_a_valid_url/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
