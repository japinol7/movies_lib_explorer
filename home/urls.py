from django.urls import path

from home.views import home_views

app_name = 'home'
urlpatterns = [
    path('sample/', home_views.sample, name='sample'),
    path('about/', home_views.about, name='about'),
]
