from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from catalog.views import actor_views
from catalog.views import director_views
from catalog.views import movie_views
from catalog.views_api.v1 import director_views_api as director_views_api_v1
from catalog.views_api.v1 import movie_views_api as movie_views_api_v1
from catalog.views_api.v1 import actor_views_api as actor_views_api_v1
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

    path('api/v1/directors/', director_views_api_v1.DirectorList.as_view(), name="api_directors"),
    path('api/v1/directors/<int:pk>/', director_views_api_v1.DirectorDetail.as_view(), name="api_director_detail"),

    path('api/v1/movies/', movie_views_api_v1.MovieList.as_view(), name="api_movies"),
    path('api/v1/movies/<int:pk>/', movie_views_api_v1.MovieDetail.as_view(), name="api_movie_detail"),

    path('api/v1/actors/', actor_views_api_v1.ActorList.as_view(), name="api_actors"),
    path('api/v1/actors/<int:pk>/', actor_views_api_v1.ActorDetail.as_view(), name="api_actor_detail"),

    path('actor_list/', actor_views.actor_list, name="actor_list"),
    path('actor/<int:actor_id>/', actor_views.actor, name="actor"),
    path('upload_actor_photo/<int:actor_id>/', actor_views.upload_actor_photo,
         name="upload_actor_photo"),
    path('calc_new_actors_from_cast/', actor_views.calc_new_actors_from_cast,
         name="calc_new_actors_from_cast"),

    path('about/', home_views.about, name="about"),
    path('load_data/', load_data_views.load_data, name="load_data"),
    ]

urlpatterns = format_suffix_patterns(urlpatterns)
