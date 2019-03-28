"""Battleships URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# Commenting these for now since Feynman isn't (yet) on Django 2.x
#from django.urls import path, re_path

from django.conf.urls import include, url

from Battleships.battleships import views

urlpatterns = [
    
    url(r'^admin/', admin.site.urls),
    url(r'^api/1.0/games/index', views.api_games_index),
    url(r'^api/1.0/games/index', views.api_games_index),
    url(r'^api/1.0/players/index', views.api_players_index),
    url(r'^api/1.0/players/register/(P?<name>[A-Za-z_]+)', views.api_players_register),
    url(r'^api/1.0/players/delete/(P?<name>[A-Za-z_]+)', views.api_players_delete),

]
