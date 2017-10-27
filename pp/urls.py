"""pp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^\$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

from general.views import Index, About, Contact

urlpatterns = [
    # Admin Urls
    # /admin/*
    url(r'^admin/', admin.site.urls),

    # Index View
    # /
    url(r'^$', Index.as_view(), name='index'),

    # About view
    # /about/
    url(r'^about/$', About.as_view(), name='about'),
    
    # Contact view
    # /contact/
    url(r'^contact/$', Contact.as_view(), name='contact'),
    
    # Games Urls
    # /games/*
    url(r'^games/', include('games.urls', namespace='games')),

    # /sellers/*
    url(r'^sellers/', include('sellers.urls', namespace='sellers')),

    # /sharing/*    
    url(r'^sharing/', include('sharing.urls', namespace='sharing')),

    # /search/*    
    url(r'^search/', include('search.urls', namespace='search')),

    # /deals/*    
    url(r'^deals/', include('deals.urls', namespace='deals')),
    
]
