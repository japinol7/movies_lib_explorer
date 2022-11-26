from django.urls import path

from catalog.views import director_views
from catalog.views import movie_views
from catalog.views_api import director_views_api
from catalog.views import load_data_views
from home.views import home_views

urlpatterns = [
    path('movie_list/', movie_views.movie_list, name='movie_list'),
    path('movie/<int:movie_id>/', movie_views.movie, name='movie'),
    path('upload_movie_photo/<int:movie_id>/', movie_views.upload_movie_photo,
         name="upload_movie_photo"),

    path('director_list/', director_views.director_list, name="director_list"),
    path('director/<int:director_id>/', director_views.director, name="director"),
    path('upload_director_photo/<int:director_id>/', director_views.upload_director_photo,
         name="upload_director_photo"),
    path('list_directors_api/', director_views_api.list_directors_api),

    path('about/', home_views.about, name="about"),
    path('load_data/', load_data_views.load_data, name="load_data"),
    ]
