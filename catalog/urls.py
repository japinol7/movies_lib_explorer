from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

from catalog.config.config import API_ACTORS_PATH, API_DIRECTORS_PATH, API_MOVIES_PATH, API_AUTH_TOKEN_PATH
from catalog.views import (
    actor_views,
    director_views,
    movie_views,
    settings_views,
    )
from catalog.views_api.v1 import director_views_api as director_views_api_v1
from catalog.views_api.v1 import movie_views_api as movie_views_api_v1
from catalog.views_api.v1 import actor_views_api as actor_views_api_v1
from catalog.views import load_data_views
from home.views import home_views

app_name = 'catalog'
urlpatterns = [
    path('settings/', settings_views.catalog_settings, name='settings'),
    path('settings_edit/<int:settings_id>/', settings_views.settings_edit_form, name='settings_edit_form'),
    path('export_movies_report/', settings_views.export_movies_report, name="export_movies_report"),

    path('movie_list/', movie_views.movie_list, name='movie_list'),
    path('movie_list_by_year/', movie_views.movie_list_by_year, name='movie_list_by_year'),
    path('movie_list_by_decade/', movie_views.movie_list_by_decade, name='movie_list_by_decade'),
    path('movie_list_by_genre/', movie_views.movie_list_by_genre, name='movie_list_by_genre'),
    path('movie_list_search/', movie_views.movie_list_search, name='movie_list_search'),
    path('movie_with_picture_list/', movie_views.movie_with_picture_list, name='movie_with_picture_list'),
    path('movie/<int:movie_id>/', movie_views.movie, name='movie'),
    path('upload_movie_photo/<int:movie_id>/', movie_views.upload_movie_photo,
         name="upload_movie_photo"),
    path('movie_create/', movie_views.movie_create_form, name='movie_create_form'),
    path('movie_delete/<int:movie_id>/', movie_views.movie_delete_form, name='movie_delete_form'),
    path('movie_edit/<int:movie_id>/', movie_views.movie_edit_form, name='movie_edit_form'),

    path("tmdb_movie_search_form/<int:movie_id>/", movie_views.tmdb_movie_search_form,
         name='tmdb_movie_search_form'),
    path("tmdb_movie_link/<int:movie_id>/", movie_views.tmdb_movie_link, name='tmdb_movie_link'),

    path('director_list/', director_views.director_list, name="director_list"),
    path('director_list_search/', director_views.director_list_search, name='director_list_search'),
    path('director/<int:director_id>/', director_views.director, name="director"),
    path('upload_director_photo/<int:director_id>/', director_views.upload_director_photo,
         name="upload_director_photo"),
    path('director_create/', director_views.director_create_form, name='director_create_form'),
    path('director_delete_not_allowed/<int:director_id>/', director_views.director_delete_not_allowed,
         name='director_delete_not_allowed'),
    path('director_delete/<int:director_id>/', director_views.director_delete_form, name='director_delete_form'),
    path('director_edit/<int:director_id>/', director_views.director_edit_form, name='director_edit_form'),

    path("tmdb_director_search_form/<int:director_id>/", director_views.tmdb_director_search_form,
         name='tmdb_director_search_form'),
    path("tmdb_director_link/<int:director_id>/", director_views.tmdb_director_link, name='tmdb_director_link'),

    path('actor_list/', actor_views.actor_list, name="actor_list"),
    path('actor_list_search/', actor_views.actor_list_search, name='actor_list_search'),
    path('actor/<int:actor_id>/', actor_views.actor, name="actor"),
    path('upload_actor_photo/<int:actor_id>/', actor_views.upload_actor_photo,
         name="upload_actor_photo"),
    path('calc_new_actors_from_cast/', actor_views.calc_new_actors_from_cast,
         name="calc_new_actors_from_cast"),
    path('actor_edit/<int:actor_id>/', actor_views.actor_edit_form, name='actor_edit_form'),

    path("tmdb_actor_search_form/<int:actor_id>/", actor_views.tmdb_actor_search_form,
         name='tmdb_actor_search_form'),
    path("tmdb_actor_link/<int:actor_id>/", actor_views.tmdb_actor_link, name='tmdb_actor_link'),

    path(API_DIRECTORS_PATH, director_views_api_v1.DirectorList.as_view(), name="api_directors"),
    path(f'{API_DIRECTORS_PATH}/', director_views_api_v1.DirectorList.as_view(), name="api_directors"),
    path(f'{API_DIRECTORS_PATH}/<int:pk>', director_views_api_v1.DirectorDetail.as_view(), name="api_director_detail"),
    path(f'{API_DIRECTORS_PATH}/<int:pk>/', director_views_api_v1.DirectorDetail.as_view(), name="api_director_detail"),

    path(API_MOVIES_PATH, movie_views_api_v1.MovieList.as_view(), name="api_movies"),
    path(f'{API_MOVIES_PATH}/', movie_views_api_v1.MovieList.as_view(), name="api_movies"),
    path(f'{API_MOVIES_PATH}/<int:pk>', movie_views_api_v1.MovieDetail.as_view(), name="api_movie_detail"),
    path(f'{API_MOVIES_PATH}/<int:pk>/', movie_views_api_v1.MovieDetail.as_view(), name="api_movie_detail"),

    path(API_ACTORS_PATH, actor_views_api_v1.ActorList.as_view(), name="api_actors"),
    path(f'{API_ACTORS_PATH}/', actor_views_api_v1.ActorList.as_view(), name="api_actors"),
    path(f'{API_ACTORS_PATH}/<int:pk>', actor_views_api_v1.ActorDetail.as_view(), name="api_actor_detail"),
    path(f'{API_ACTORS_PATH}/<int:pk>/', actor_views_api_v1.ActorDetail.as_view(), name="api_actor_detail"),

    path(API_AUTH_TOKEN_PATH, obtain_auth_token),

    path('about/', home_views.about, name="about"),
    path('load_data/', load_data_views.load_data, name="load_data"),
    ]

urlpatterns = format_suffix_patterns(urlpatterns)
