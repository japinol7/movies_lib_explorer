"""movies_lib_explorer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
# from django.views.generic.base import RedirectView

import debug_toolbar

from home.views import home_views as home_views

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),
    path('home/', include('home.urls')),
    path('', home_views.home),
    path('catalog/', include('catalog.urls')),
    path('users/', include('users.urls')),
    path('review/', include('review.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
    path('api-auth/', include('rest_framework.urls')),
    ]

# WARNING: In production, you should use nginx or another similar tool to serve files, instead of Django
# Do not use Django to serve media files in production.
# It should be handled by web server, similar to static files.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
