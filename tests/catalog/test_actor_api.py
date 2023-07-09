import json

from django.contrib import admin
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from catalog.models.actor import Actor
from users.models.user import User
from tools.logger.logger import log


class ActorAPITestCase(APITestCase):
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

        self.actor = Actor.objects.create(last_name='Toshiro Mifune', first_name='Dummy')
        self.actor_count = Actor.objects.count()

        self.client = APIClient()

    def _log_as_user(self):
        log.info("Log as user")
        self.client.login(username=self.user.username, password=self.USER_PASSWORD)

    def _log_as_admin_user(self):
        log.info("Log as admin user")
        self.client.force_authenticate(user=self.admin_user, token=self.admin_user.auth_token)

    def test_get_actor_list(self):
        log.info("Get actor list")
        response = self.client.get(
            path=reverse('catalog:api_actors'),
            content_type='application/json')
        json_data = response.json()
        actor = json_data['results'][-1]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(actor['last_name'], self.actor.last_name)
        self.assertEqual(actor['first_name'], self.actor.first_name)

    def test_get_actor_list_filtered_by_last_name(self):
        log.info("Get actor list filtered by last name")
        Actor.objects.create(last_name='Toshiro Mifune', first_name='Dummy')
        Actor.objects.create(last_name='Cary Grant')

        search_name = 'Toshiro Mifune'
        response = self.client.get(
            path=rf"http://127.0.0.1:8000/catalog/api/v1/actors/?last_name={search_name}",
            content_type='application/json')
        json_data = response.json()
        actors = json_data['results']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(actors), 2)
        self.assertEqual(actors[0]['last_name'], self.actor.last_name)
        self.assertEqual(actors[0]['first_name'], self.actor.first_name)
        self.assertEqual(actors[1]['last_name'], 'Toshiro Mifune')
        self.assertEqual(actors[1]['first_name'], 'Dummy')

    def test_get_actor_list_filter_first_name_and_order_last_name(self):
        log.info("Get actor list filtered by first name and ordered by last name")
        Actor.objects.create(last_name='Jean Harlow', first_name='Dummy_2')
        Actor.objects.create(last_name='Jean Arthur', first_name='Dummy_2')

        search_name = 'Dummy_2'
        response = self.client.get(
            path=rf"http://127.0.0.1:8000/catalog/api/v1/actors/?first_name={search_name}&ordering=last_name",
            content_type='application/json')
        json_data = response.json()
        actors = json_data['results']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(actors), 2)
        self.assertEqual(actors[0]['last_name'], 'Jean Arthur')
        self.assertEqual(actors[0]['first_name'], 'Dummy_2')
        self.assertEqual(actors[1]['last_name'], 'Jean Harlow')
        self.assertEqual(actors[1]['first_name'], 'Dummy_2')

    def test_get_actor_list_search_first_name_and_order_last_name(self):
        log.info("Get actor list searched by first name and ordered by last name")
        Actor.objects.create(last_name='Jeanne Cagney', first_name='Dummy')
        Actor.objects.create(last_name='Jean Harlow', first_name='Dummy')
        Actor.objects.create(last_name='Dummy', first_name='Dummy')
        Actor.objects.create(last_name='Jean Arthur', first_name='Dummy')

        search_name = 'Jean'
        response = self.client.get(
            path=rf"http://127.0.0.1:8000/catalog/api/v1/actors/?search={search_name}&ordering=last_name",
            content_type='application/json')
        json_data = response.json()
        actors = json_data['results']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(actors), 3)
        self.assertEqual(actors[0]['last_name'], 'Jean Arthur')
        self.assertEqual(actors[0]['first_name'], 'Dummy')
        self.assertEqual(actors[1]['last_name'], 'Jean Harlow')
        self.assertEqual(actors[1]['first_name'], 'Dummy')
        self.assertEqual(actors[2]['last_name'], 'Jeanne Cagney')
        self.assertEqual(actors[2]['first_name'], 'Dummy')

    def test_get_actor_detail(self):
        log.info("Get actor detail")
        response = self.client.get(
            path=rf"http://127.0.0.1:8000/catalog/api/v1/actors/{self.actor.id}/",
            content_type='application/json')
        json_data = response.json()
        actor = json_data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(actor['last_name'], self.actor.last_name)
        self.assertEqual(actor['first_name'], self.actor.first_name)

    def test_update_actor_detail(self):
        self._log_as_admin_user()
        log.info("Update actor detail")
        vals = {
            'last_name': f"{self.actor.last_name} Updated",
            'first_name': f"{self.actor.first_name} Updated",
            }
        response = self.client.put(
            path=rf"http://127.0.0.1:8000/catalog/api/v1/actors/{self.actor.id}/",
            content_type='application/json',
            data=json.dumps(vals))
        json_data = response.json()
        actor = json_data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(actor['last_name'], f"{self.actor.last_name} Updated")
        self.assertEqual(actor['first_name'], f"{self.actor.first_name} Updated")

    def test_delete_actor(self):
        self._log_as_admin_user()
        log.info("Delete actor")
        response = self.client.delete(
            path=rf"http://127.0.0.1:8000/catalog/api/v1/actors/{self.actor.id}/",
            content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Actor.objects.count(), self.actor_count - 1)

    def test_create_actor(self):
        self._log_as_admin_user()
        log.info("Create actor")
        vals = {
            'last_name': 'Test-Actor-Last_Name',
            'first_name': 'Test-Actor-First_Name',
            }
        response = self.client.post(
            path=reverse('catalog:api_actors'),
            content_type='application/json',
            data=json.dumps(vals))
        json_data = response.json()
        log.info(f"Create actor Response json: {json_data}")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_data['last_name'], 'Test-Actor-Last_Name')
        self.assertEqual(Actor.objects.count(), self.actor_count + 1)
