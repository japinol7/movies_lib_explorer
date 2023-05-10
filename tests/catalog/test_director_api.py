from django.contrib import admin
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from catalog.models.director import Director
from users.models.user import User
from tools.logger.logger import log


class DirectorAPITestCase(APITestCase):
    ADMIN_USER = "admin"
    ADMIN_EMAIL = "admin@ex.com"
    ADMIN_PASSWORD = "aD*mi@n_pw2d"
    USER_PASSWORD = 'test_asPg*f33'
    MLME_REST_API_TOKEN = "test_N.PviF82fxGL;k9R3L-4Hxv@J"

    def setUp(self):
        super().setUp()

        log.info("Create user and admin user")
        self.user = User.objects.create_user(f'testy', f'testy@example.com', self.USER_PASSWORD)
        self.site = admin.sites.AdminSite()
        self.admin_user = User.objects.create_user(
            self.ADMIN_USER, self.ADMIN_EMAIL, self.ADMIN_PASSWORD)
        self.admin_user.is_staff = True
        self.admin_user.is_superuser = True
        self.admin_user.save()

        self.director = Director.objects.create(last_name="Kurusawa")
        self.director_count = Director.objects.count()

        self.client = APIClient()

    def _log_as_user(self):
        log.info("Log as user")
        self.client.login(username=self.user.username, password=self.USER_PASSWORD)
        self.credentials = {'Authorization': f"Token {self.MLME_REST_API_TOKEN}"}

    def _log_as_admin_user(self):
        log.info("Log as admin user")
        self.client.login(username=self.admin_user.username, password=self.ADMIN_PASSWORD)
        self.credentials = {'Authorization': f"Token {self.MLME_REST_API_TOKEN}"}

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

    def test_create_director(self):
        self._log_as_admin_user()
        log.info("Create director")
        vals = {
            'last_name': 'Test-Director-Last_Name',
            'first_name': 'Test-Director-First_Name',
            },

        response = self.client.post(
            path=reverse('api_directors'),
            content_type='application/json',
            data=vals)
        json_data = response.json()
        log.info(f"Create director Response json: {json_data}")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_data['last_name'], 'Test-Director-Last_Name')
        self.assertEqual(Director.objects.count(), self.director_count + 1)
