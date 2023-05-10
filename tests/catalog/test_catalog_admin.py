from django.contrib import admin
from django.contrib.admin.utils import lookup_field
from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client

from catalog.admin import DirectorAdmin
from catalog.models.director import Director


class CatalogAdminTestCase(TestCase):
    ADMIN_USER = "admin"
    ADMIN_EMAIL = "admin@ex.com"
    ADMIN_PASSWORD = "aD*mi@n_pw2d"

    def setUp(self):
        super().setUp()
        self.site = admin.sites.AdminSite()
        self.admin_user = User.objects.create_user(
            self.ADMIN_USER, self.ADMIN_EMAIL, self.ADMIN_PASSWORD)
        self.admin_user.is_staff = True
        self.admin_user.is_superuser = True
        self.admin_user.save()
        self.client = Client()

    def test_movie_listing(self):
        # Authenticate as admin user
        response = self.client.login(
            username=self.ADMIN_USER, password=self.ADMIN_PASSWORD)
        self.assertTrue(response)

        # Fetch movie listing page
        response = self.client.get("/admin/catalog/movie/")
        self.assertEqual(response.status_code, 200)

        # Check show_movies field
        director = Director.objects.create(last_name="Test_Director")
        director_admin = DirectorAdmin(director, self.site)
        _, _, value = lookup_field("show_movies", director, director_admin)
        expected = f"?director__id={director.id}"
        self.assertIn(expected, value)
