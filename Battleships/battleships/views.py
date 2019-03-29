from django.shortcuts import get_object_or_404, render

import json

from django.http import HttpResponse
from django.http import JsonResponse

from django.core import serializers


from django.template import loader

from .models import Player, Game, Ship, Action

# Create your views here.

def homepage(request):
    games = Game.objects.all()
    return render(request, 'homepage.html', {'games': games})


def api_players_index(request):
    """Show a list of players, encoded in JSON"""

    players = list(Player.objects.values())
    return render(request, 'players.html', {'players': players})


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


def api_games_add(request, game, name):
    """Attempt to add players to a game"""

    game = Game.objects.get(name=game)
    player = Player.objects.get(name=name)

    if not player:
        return JsonResponse(False, safe=False)
    if not game:
        return JsonResponse(False, safe=False)
    else:
        game.players.set(player)
        return JsonResponse(True, safe=False)


def api_game_start(request, game):
    """Attempt to start a game"""

    game = Game.objects.get(name=game)

    if not game:
        return JsonResponse(False, safe=False)
    else:
        return JsonResponse(True, safe=False)


def api_game_history(request, game):
    """Attempt to show current moves in a game"""

    game = Game.objects.get(name=game)

    if not game:
        return JsonResponse(False, safe=False)
    else:
        return JsonResponse(True, safe=False)


def api_strike(request, game, player, x, y):
    """Attempt to strike another player"""

    game = Game.objects.get(name=game)
    player = Player.objects.get(name=player)

    if not player:
        return JsonResponse(False, safe=False)
    if not game:
        return JsonResponse(False, safe=False)
    else:
        return JsonResponse(True, safe=False)
