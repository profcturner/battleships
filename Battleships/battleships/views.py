from django.shortcuts import render

import json

from django.http import HttpResponse
from django.http import JsonResponse

from django.core import serializers


from django.template import loader

from .models import Player
from .models import Game

# Create your views here.

def api_players_index(request):
    """Show a list of games, encoded in JSON"""

    games = list(Player.objects.values())
    return JsonResponse(games, safe=False)


def api_players_register(request, name):
    """Attempt to register a name"""

    player = Player.objects.create(name=name)
    return JsonResponse(True, safe=False)


def api_players_delete(request, name):
    """Attempt to register a name"""

    player = Player.objects.get(name=name)
    if not player:
        return JsonResponse(False, safe=False)
    else:
        player.delete()
        return JsonResponse(True, safe=False)


def api_games_index(request):
    """Show a list of games, encoded in JSON"""

    games = list(Game.objects.values())
    return JsonResponse(games, safe=False)

