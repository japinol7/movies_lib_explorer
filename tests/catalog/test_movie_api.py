import datetime
import json

from django.contrib import admin
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from catalog.models.movie import Director
from catalog.models.movie import Movie
from users.models.user import User
from tools.logger.logger import log


class MovieAPITestCase(APITestCase):
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

        self.director = Director.objects.create(last_name='Hawks', first_name='Howard')
        self.movie = Movie.objects.create(
            title="Bringing Up Baby",
            title_original="Bringing Up Baby",
            director=self.director,
            runtime=102,
            year=1938,
            country='US',
            language='English',
            cast="Cary Grant, Katherine Hepburn, Charlie Ruggles, May Robson, Walter Catlett",
            )
        self.movie_count = Movie.objects.count()

        self.client = APIClient()

    def _log_as_user(self):
        log.info("Log as user")
        self.client.login(username=self.user.username, password=self.USER_PASSWORD)

    def _log_as_admin_user(self):
        log.info("Log as admin user")
        self.client.force_authenticate(user=self.admin_user, token=self.admin_user.auth_token)

    def test_get_movie_list(self):
        log.info("Get movie list")
        response = self.client.get(
            path=reverse('catalog:api_movies'),
            content_type='application/json')
        json_data = response.json()
        movie = json_data['results'][-1]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(movie['title'], self.movie.title)
        self.assertEqual(movie['director'], self.director.id)
        self.assertEqual(movie['runtime'], self.movie.runtime)
        self.assertEqual(movie['year'], self.movie.year)
        self.assertEqual(movie['country'], self.movie.country)
        self.assertEqual(movie['cast'], self.movie.cast)

    def test_get_movie_list_filtered_by_year(self):
        log.info("Get movie list filtered by year")
        director_kurosawa = Director.objects.create(last_name='Kurusawa', first_name='Akira')
        director_capra = Director.objects.create(last_name='Capra', first_name='Frank')
        Movie.objects.create(
            title="Seven Samurai",
            director=director_kurosawa,
            runtime=205,
            year=1954,
            )
        Movie.objects.create(
            title="It Happened One Night",
            director=director_capra,
            runtime=101,
            year=1938,
            )
        self.movie_count = Movie.objects.count()

        search_year = 1938
        response = self.client.get(
            path=rf"http://127.0.0.1:8000/catalog/api/v1/movies/?year={search_year}",
            content_type='application/json')
        json_data = response.json()
        movies = json_data['results']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(movies), 2)

        self.assertEqual(movies[0]['title'], self.movie.title)
        self.assertEqual(movies[0]['director'], self.movie.director.id)
        self.assertEqual(movies[0]['runtime'], self.movie.runtime)
        self.assertEqual(movies[0]['year'], self.movie.year)

        self.assertEqual(movies[1]['title'], "It Happened One Night")
        self.assertEqual(movies[1]['director'], director_capra.id)
        self.assertEqual(movies[1]['runtime'], 101)
        self.assertEqual(movies[1]['year'], 1938)

    def test_get_movie_list_filter_year_and_order_director_last_name(self):
        log.info("Get movie list filtered by year and ordered by director's last name")
        director_kurosawa = Director.objects.create(last_name='Kurusawa', first_name='Akira')
        director_capra = Director.objects.create(last_name='Capra', first_name='Frank')
        Movie.objects.create(
            title="Seven Samurai",
            director=director_kurosawa,
            runtime=205,
            year=1954,
            )
        Movie.objects.create(
            title="It Happened One Night",
            director=director_capra,
            runtime=101,
            year=1938,
            )
        self.movie_count = Movie.objects.count()

        search_year = 1938
        response = self.client.get(
            path=rf"http://127.0.0.1:8000/catalog/api/v1/movies/?year={search_year}&ordering=director__last_name",
            content_type='application/json')
        json_data = response.json()
        movies = json_data['results']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(movies), 2)

        self.assertEqual(movies[0]['title'], "It Happened One Night")
        self.assertEqual(movies[0]['director'], director_capra.id)
        self.assertEqual(movies[0]['runtime'], 101)
        self.assertEqual(movies[0]['year'], 1938)

        self.assertEqual(movies[1]['title'], self.movie.title)
        self.assertEqual(movies[1]['director'], self.movie.director.id)
        self.assertEqual(movies[1]['runtime'], self.movie.runtime)
        self.assertEqual(movies[1]['year'], self.movie.year)

    def test_get_movie_list_filtered_by_year_range(self):
        log.info("Get movie list filtered by year greater than 1922 and lower than 1924")
        Movie.objects.create(
            title="His Girl Friday",
            director=self.director,
            runtime=92,
            year=1940,
            )
        Movie.objects.create(
            title="To Have and Have Not",
            director=self.director,
            runtime=96,
            year=1944,
            )
        Movie.objects.create(
            title="Rio Bravo",
            director=self.director,
            runtime=141,
            year=1959,
            )
        self.movie_count = Movie.objects.count()

        search_year_gt, search_year_lt = 1939, 1959
        url_path = rf"http://127.0.0.1:8000/catalog/api/v1/movies/" \
                   rf"?year__gt={search_year_gt}&year__lt={search_year_lt}&ordering=year"
        response = self.client.get(
            path=url_path,
            content_type='application/json')
        json_data = response.json()
        movies = json_data['results']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(movies), 2)

        self.assertEqual(movies[0]['title'], "His Girl Friday")
        self.assertEqual(movies[0]['runtime'], 92)
        self.assertEqual(movies[0]['year'], 1940)

        self.assertEqual(movies[1]['title'], "To Have and Have Not")
        self.assertEqual(movies[1]['runtime'], 96)
        self.assertEqual(movies[1]['year'], 1944)

    def test_get_movie_list_filtered_creation_date(self):
        log.info("Get movie list filtered by creation date")
        m2 = Movie.objects.create(
            title="His Girl Friday",
            director=self.director,
            runtime=92,
            year=1940,
            )
        m3 = Movie.objects.create(
            title="To Have and Have Not",
            director=self.director,
            runtime=96,
            year=1944,
            )
        m4 = Movie.objects.create(
            title="Rio Bravo",
            director=self.director,
            runtime=141,
            year=1959,
            )
        self.movie_count = Movie.objects.count()

        self.datetime_now = timezone.now()
        datetime_now_minus_5_days = self.datetime_now - datetime.timedelta(days=5)
        datetime_now_plus_5_days = self.datetime_now + datetime.timedelta(days=5)

        # We do this because auto_now_add and auto_now fields cannot be updated normally
        Movie.objects.filter(pk=self.movie.id).update(created=self.datetime_now)
        Movie.objects.filter(pk=m2.id).update(created=datetime_now_minus_5_days)
        Movie.objects.filter(pk=m3.id).update(created=self.datetime_now)
        Movie.objects.filter(pk=m4.id).update(created=datetime_now_plus_5_days)

        search_created_date = datetime.datetime.strftime(self.datetime_now, "%Y-%m-%d")
        url_path = rf"http://127.0.0.1:8000/catalog/api/v1/movies/" \
                   rf"?created__date={search_created_date}"
        response = self.client.get(
            path=url_path,
            content_type='application/json')
        json_data = response.json()
        movies = json_data['results']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(movies), 2)

        self.assertEqual(movies[0]['title'], "Bringing Up Baby")
        self.assertEqual(movies[0]['runtime'], 102)
        self.assertEqual(movies[0]['year'], 1938)

        self.assertEqual(movies[1]['title'], "To Have and Have Not")
        self.assertEqual(movies[1]['runtime'], 96)
        self.assertEqual(movies[1]['year'], 1944)

    def test_get_movie_list_filtered_by_director_id(self):
        log.info("Get movie list filtered by director id")
        director_kurosawa = Director.objects.create(last_name='Kurusawa', first_name='Akira')
        director_capra = Director.objects.create(last_name='Capra', first_name='Frank')
        Movie.objects.create(
            title="Seven Samurai",
            director=director_kurosawa,
            runtime=205,
            year=1954,
            )
        Movie.objects.create(
            title="It Happened One Night",
            director=director_capra,
            runtime=101,
            year=1938,
            )
        Movie.objects.create(
            title="Ikiru",
            director=director_kurosawa,
            runtime=143,
            year=1952,
            )
        self.movie_count = Movie.objects.count()

        search_director_id = director_kurosawa.id
        response = self.client.get(
            path=rf"http://127.0.0.1:8000/catalog/api/v1/movies/?director__id={search_director_id}&ordering=id",
            content_type='application/json')
        json_data = response.json()
        movies = json_data['results']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(movies), 2)

        self.assertEqual(movies[0]['title'], "Seven Samurai")
        self.assertEqual(movies[0]['director'], director_kurosawa.id)
        self.assertEqual(movies[0]['runtime'], 205)
        self.assertEqual(movies[0]['year'], 1954)

        self.assertEqual(movies[1]['title'], "Ikiru")
        self.assertEqual(movies[1]['director'], director_kurosawa.id)
        self.assertEqual(movies[1]['runtime'], 143)
        self.assertEqual(movies[1]['year'], 1952)

    def test_get_movie_list_search_how__must_found_2_movies(self):
        log.info("Get movie list searching for 'how' and ordered by year in descending order")
        director_ford = Director.objects.create(last_name='Ford', first_name='John')
        director_howard = Director.objects.create(last_name='Howard', first_name='Ron')
        Movie.objects.create(
            title="She Wore a Yellow Ribbon",
            director=director_ford,
            runtime=103,
            year=1949,
            )
        Movie.objects.create(
            title=r"Frost/Nixon",
            director=director_howard,
            runtime=122,
            year=2008,
            )
        self.movie_count = Movie.objects.count()

        search_text = 'how'
        response = self.client.get(
            path=rf"http://127.0.0.1:8000/catalog/api/v1/movies/?search={search_text}&ordering=-year",
            content_type='application/json')
        json_data = response.json()
        movies = json_data['results']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(movies), 2)

        self.assertEqual(movies[0]['title'], r"Frost/Nixon")
        self.assertEqual(movies[0]['director'], director_howard.id)
        self.assertEqual(movies[0]['runtime'], 122)
        self.assertEqual(movies[0]['year'], 2008)

        self.assertEqual(movies[1]['title'], self.movie.title)
        self.assertEqual(movies[1]['director'], self.movie.director.id)
        self.assertEqual(movies[1]['runtime'], self.movie.runtime)
        self.assertEqual(movies[1]['year'], self.movie.year)

    def test_get_movie_detail(self):
        log.info("Get movie detail")
        response = self.client.get(
            path=rf"http://127.0.0.1:8000/catalog/api/v1/movies/{self.movie.id}/",
            content_type='application/json')
        json_data = response.json()
        movie = json_data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(movie['title'], self.movie.title)
        self.assertEqual(movie['title_original'], self.movie.title)
        self.assertEqual(movie['director'], self.movie.director.id)
        self.assertEqual(movie['director_data']['last_name'], self.movie.director.last_name)
        self.assertEqual(movie['runtime'], self.movie.runtime)
        self.assertEqual(movie['year'], self.movie.year)
        self.assertEqual(movie['country'], self.movie.country)
        self.assertEqual(movie['language'], self.movie.language)
        self.assertEqual(movie['cast'], self.movie.cast)

    def test_update_movie_detail(self):
        self._log_as_admin_user()
        log.info("Update movie detail")
        vals = {
            'title': f"{self.movie.title} Updated",
            'title_original': f"{self.movie.title_original} Updated",
            'year': self.movie.year + 100,
            }
        response = self.client.put(
            path=rf"http://127.0.0.1:8000/catalog/api/v1/movies/{self.movie.id}/",
            content_type='application/json',
            data=json.dumps(vals))
        json_data = response.json()
        movie = json_data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(movie['title'], f"{self.movie.title} Updated")
        self.assertEqual(movie['title_original'], f"{self.movie.title_original} Updated")
        self.assertEqual(movie['year'], self.movie.year + 100)

    def test_delete_movie(self):
        self._log_as_admin_user()
        log.info("Delete movie")
        response = self.client.delete(
            path=rf"http://127.0.0.1:8000/catalog/api/v1/movies/{self.movie.id}/",
            content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Movie.objects.count(), self.movie_count - 1)

    def test_create_movie(self):
        self._log_as_admin_user()
        log.info("Create movie")
        vals = {
            'title': "Test: A Story of Floating Weeds",
            'title_original': "Test: Ukikusa monogatari",
            'director': 1,
            'year': 1934,
            'runtime': 86,
            'country': 'JP',
            'language': 'Japanese',
            'cast': "Takeshi Sakamoto, Chōko Iida, Kōji Mitsui, Rieko Yagumo, Yoshiko Tsubouchi",
            }
        response = self.client.post(
            path=reverse('catalog:api_movies'),
            content_type='application/json',
            data=json.dumps(vals))
        json_data = response.json()
        log.info(f"Create movie Response json: {json_data}")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), self.movie_count + 1)

        self.assertEqual(json_data['title'], vals['title'])
        self.assertEqual(json_data['title_original'], vals['title_original'])
        self.assertEqual(json_data['director'], vals['director'])
        self.assertEqual(json_data['year'], vals['year'])
        self.assertEqual(json_data['runtime'], vals['runtime'])
        self.assertEqual(json_data['country'], vals['country'])
        self.assertEqual(json_data['language'], vals['language'])
        self.assertEqual(json_data['cast'], vals['cast'])
