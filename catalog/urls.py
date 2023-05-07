from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from catalog.views import director_views
from catalog.views import movie_views
from catalog.views_api.v1 import director_views_api as director_views_api_v1
from catalog.views import load_data_views
from home.views import home_views

urlpatterns = [
    path('movie_list/', movie_views.movie_list, name='movie_list'),
    path('movie_with_picture_list/', movie_views.movie_with_picture_list, name='movie_with_picture_list'),
    path('movie/<int:movie_id>/', movie_views.movie, name='movie'),
    path('upload_movie_photo/<int:movie_id>/', movie_views.upload_movie_photo,
         name="upload_movie_photo"),

    path('director_list/', director_views.director_list, name="director_list"),
    path('director/<int:director_id>/', director_views.director, name="director"),
    path('upload_director_photo/<int:director_id>/', director_views.upload_director_photo,
         name="upload_director_photo"),

    path('api/v1/directors/', director_views_api_v1.DirectorList.as_view()),
    path('api/v1/directors/<int:pk>/', director_views_api_v1.DirectorDetail.as_view(), name="director"),

    path('about/', home_views.about, name="about"),
    path('load_data/', load_data_views.load_data, name="load_data"),
    ]

urlpatterns = format_suffix_patterns(urlpatterns)
