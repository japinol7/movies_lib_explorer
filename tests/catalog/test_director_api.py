import json

from django.contrib import admin
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

from catalog.models.director import Director
from users.models.user import User
from tools.logger.logger import log


class DirectorAPITestCase(APITestCase):
    ADMIN_USER = "admin"
    ADMIN_EMAIL = "admin@ex.com"
    ADMIN_PASSWORD = "aD*mi@n_pw2d"
    USER_PASSWORD = 'test_asPg*f33'

    def setUp(self):
        super().setUp()

        log.info("Create user and admin user")
        self.user = User.objects.create_user(f'testy', f'testy@example.com', self.USER_PASSWORD)
        self.site = admin.sites.AdminSite()
        self.admin_user = User.objects.create_user(
            self.ADMIN_USER, self.ADMIN_EMAIL, self.ADMIN_PASSWORD)
        self.admin_user.is_staff = True
        self.admin_user.is_superuser = True
        self.admin_auth_token = Token.objects.create(user=self.admin_user)
        self.admin_user.save()

        self.director = Director.objects.create(last_name='Kurusawa', first_name='Akira')
        self.director_count = Director.objects.count()

        self.client = APIClient()

    def _log_as_user(self):
        log.info("Log as user")
        self.client.login(username=self.user.username, password=self.USER_PASSWORD)

    def _log_as_admin_user(self):
        log.info("Log as admin user")
        self.client.force_authenticate(user=self.admin_user, token=self.admin_user.auth_token)

    def test_get_director_list(self):
        log.info("Get director list")
        response = self.client.get(
            path=reverse('api_directors'),
            content_type='application/json')
        json_data = response.json()
        director = json_data[-1]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(director['last_name'], self.director.last_name)
        self.assertEqual(director['first_name'], self.director.first_name)

    def test_get_director_detail(self):
        log.info("Get director detail")
        response = self.client.get(
            path=rf"http://127.0.0.1:8000/catalog/api/v1/directors/{self.director.id}/",
            content_type='application/json')
        json_data = response.json()
        director = json_data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(director['last_name'], self.director.last_name)
        self.assertEqual(director['first_name'], self.director.first_name)

    def test_update_director_detail(self):
        self._log_as_admin_user()
        log.info("Update director detail")
        vals = {
            'last_name': f"{self.director.last_name} Updated",
            'first_name': f"{self.director.first_name} Updated",
            }
        response = self.client.put(
            path=rf"http://127.0.0.1:8000/catalog/api/v1/directors/{self.director.id}/",
            content_type='application/json',
            data=json.dumps(vals))
        json_data = response.json()
        director = json_data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(director['last_name'], f"{self.director.last_name} Updated")
        self.assertEqual(director['first_name'], f"{self.director.first_name} Updated")

    def test_delete_director_detail(self):
        self._log_as_admin_user()
        log.info("Delete director")
        response = self.client.delete(
            path=rf"http://127.0.0.1:8000/catalog/api/v1/directors/{self.director.id}/",
            content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Director.objects.count(), self.director_count - 1)
