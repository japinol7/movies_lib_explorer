from django.urls import path

from review.views import review_views

app_name = 'review'
urlpatterns = [
    path('review_movie/<int:movie_id>/', review_views.review_movie, name="review_movie"),
]
