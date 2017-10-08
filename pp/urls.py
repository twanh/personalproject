"""pp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    # Admin Urls
    # /admin/*
    url(r'^admin/', admin.site.urls),

    # Index View
    # /
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),

    # Games Urls
    # /games/
    url(r'^games/', include('games.urls', namespace='games')),

    url(r'^sellers/', include('sellers.urls', namespace='sellers')),
    url(r'^sharing/', include('sharing.urls', namespace='sharing')),

    url(r'^search/', include('search.urls', namespace='search')),
]
