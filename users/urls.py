from django.urls import path

from users.views import user_profile_views

urlpatterns = [
    path('profile_listing/', user_profile_views.profile_listing),
    path('profile/<int:profile_id>/', user_profile_views.profile),
    ]
