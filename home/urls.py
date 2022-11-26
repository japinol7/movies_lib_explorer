from django.urls import path

from home.views import home_views

urlpatterns = [
    path('sample/', home_views.sample),
    path('about/', home_views.about),
]
