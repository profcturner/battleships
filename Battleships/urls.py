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
from django.urls import path, re_path

from django.conf.urls import include

from server import views

urlpatterns = [

    re_path(r'^admin/', admin.site.urls),
    re_path(r'^$', views.index),
    re_path(r'^view_game/(?P<game_name>\w+)/$', views.view_game, name="view_game"),
    re_path(r'^view_game/(?P<game_name>\w+)/(?P<player_id>\w+)/$', views.view_game),
    re_path(r'^view_game/(?P<game_name>\w+)/(?P<player_name>\w+)/(?P<secret>\w+)/$', views.view_game),
    re_path(r'^api/1.0/players/index/$', views.api_players_index),
    re_path(r'^api/1.0/players/register/(?P<player_name>\w+)/$', views.api_players_register),
    re_path(r'^api/1.0/players/delete/(?P<player_name>\w+)/(?P<secret>\w+)/$', views.api_players_delete),
    re_path(r'^api/1.0/games/index/$', views.api_games_index),
    re_path(r'^api/1.0/games/register/(?P<game_name>\w+)/$', views.api_games_register),
    re_path(r'^api/1.0/games/delete/(?P<game_name>\w+)/(?P<secret>\w+)/$', views.api_games_delete),
    re_path(r'^api/1.0/games/addplayer/(?P<game_name>\w+)/(?P<player_name>\w+)/$', views.api_games_add_player),
    re_path(r'^api/1.0/games/start/(?P<game_name>\w+)/$', views.api_games_start_game),
    re_path(r'^api/1.0/games/history/(?P<game_name>\w+)/$', views.api_games_history),
    re_path(r'^api/1.0/games/getships/(?P<game_name>\w+)/(?P<player_name>\w+)/(?P<secret>\w+)/$', views.api_games_getships),
    re_path(r'^api/1.0/games/getwinner/(?P<game_name>\w+)/$', views.api_games_getwinner),
    re_path(r'^api/1.0/strike/(?P<game_name>\w+)/(?P<player_name>\w+)/\((?P<x>[0-9]+),(?P<y>[0-9]+)\)/(?P<secret>\w+)/$', views.api_strike),

]
