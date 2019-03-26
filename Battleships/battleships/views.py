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
    """Show a list of players, encoded in JSON"""

    players = list(Player.objects.values())
    return JsonResponse(players, safe=False)


def api_players_register(request, name):
    """Attempt to register a player name"""

    player = Player.objects.create(name=name)
    return JsonResponse(True, safe=False)


def api_players_delete(request, name):
    """Attempt to delete a player"""

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


def api_games_register(request, name):
    """"Attempt to register a game"""

    game = Game.objects.create(name=name)
    return JsonResponse(True, safe=False)


def api_games_delete(request, name):
    """Attempt to delete a game"""

    game = Game.objects.get(name=name)
    if not game:
        return JsonResponse(False, safe=False)
    else:
        game.delete()
        return JsonResponse(True, safe=False)


def api_games_add(request, name, name1, name2):
    """Attempt to add players to a game"""

    game = Game.objects.get(name=name)
    player1 = Player.objects.get(name=name1)
    player2 = Player.objects.get(name=name2)
    players = list(player1,player2)

    if not player1:
        return JsonResponse(False, safe=False)
    if not player2:
        return JsonResponse(False, safe=False)
    if not game:
        return JsonResponse(False, safe=False)
    else:
        game.players=player1
        return JsonResponse(True, safe=False)
