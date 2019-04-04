
from django.http import JsonResponse
# We will sometimes raise exceptions
from django.core.exceptions import PermissionDenied

from .models import Player
from .models import Game

# There are v1.0 APIs, all JSON encoded.
# In many of these views all exceptions are caught, this is to avoid exposing them to hostile end users


def api_players_index(request):
    """Show a list of games, encoded in JSON"""

    try:
        players = Player.list_players_as_dicts()
        response = players
        status_code = 200
    except:
        response = "Unknown Error"
        status_code = 500

    return JsonResponse(response, safe=False, status=status_code)


def api_players_register(request, player_name):
    """Attempt to register a name"""

    try:
        # Add the player
        player = Player.objects.create(name=player_name)
        # Then generate a secret
        response = player.create_secret()
        # Signal that all went well
        status_code = 200
    except:
        response = f"Could not create player {player_name}"
        status_code = 403

    return JsonResponse(response, safe=False, status=status_code)


def api_players_delete(request, player_name, secret):
    """Attempt to delete a player with its secret"""

    try:
        # Fetch the player
        player = Player.objects.get(name=player_name)
        if not player:
            status_code = 404
            response = f"Could not find player {player_name}"
        else:
            if secret != player.get_secret():
                status_code = 403
                response = f"Invalid secret"
            else:
                # We have a player and valid secret
                player.delete()
                status_code = 200
                response = f"Player {player_name} deleted"

        return JsonResponse(response, safe=False, status=status_code)
    except:
        status_code = 500
        return JsonResponse("Unknown error", safe=False, status=status_code)


def api_games_index(request):
    """Show a list of games"""

    try:
        games = Game.list_games_as_dicts()
        response = games
        status_code = 200
    except:
        response = "Unknown Error"
        status_code = 500

    return JsonResponse(response, safe=False, status=status_code)


def api_games_register(request, game_name):
    """Attempt to register a new game"""

    try:
        # Add the game
        game = Game.objects.create(name=game_name)
        # Then generate a secret
        response = game.create_secret()
        # Signal that all went well
        status_code = 200
    except:
        response = f"Could not create game {game_name}"
        status_code = 403

    return JsonResponse(response, safe=False, status=status_code)


def api_games_delete(request, game_name, secret):
    """Attempt to delete a game with a valid secret"""

    try:
        # Fetch the game
        game = Game.objects.get(name=game_name)
        if not game:
            status_code = 404
            response = f"Could not find game {game_name}"
        else:
            if secret != game.get_secret():
                status_code = 403
                response = f"Invalid secret"
            else:
                # We have a player and valid secret
                game.delete()
                status_code = 200
                response = f"Game {game_name} deleted"

        return JsonResponse(response, safe=False, status=status_code)

    except:
        status_code = 500
        return JsonResponse("Unknown error", safe=False, status=status_code)


def api_games_add_player(request, game_name, player_name):
    """Add a player into a game"""

    try:
        # Fetch the game
        game = Game.objects.get(name=game_name)
        if not game:
            status_code = 404
            response = f"Could not find game {game_name}"

        # Fetch the player
        player = Player.objects.get(name=player_name)
        if not player:
            status_code = 404
            response = f"Could not find player {player_name}"

        # Have we both?
        if game and player:
            # Is it already there
            if player in game.players.all():
                status_code = 403
                response = f"Player {player_name} is already in game {game_name}"

            # Or are there already ships?
            elif game.number_of_ships():
                status_code = 403
                response = "Game already started"

            else:
                # Add it
                game.players.add(player)
                game.save()
                status_code = 200
                response = f"Player {player_name} added to {game_name}"

        return JsonResponse(response, safe=False, status=status_code)

    except:
        status_code = 500
        return JsonResponse("Unknown error", safe=False, status=status_code)


def api_games_start_game(request, game_name):
    """Generate ships ready to go"""

    try:
        # Fetch the game
        game = Game.objects.get(name=game_name)
        if not game:
            status_code = 404
            response = f"Could not find game {game_name}"
        else:
            # Are there ships already?
            if game.number_of_ships():
                # Disallow further ship generation
                status_code = 403
                response = "GameAlreadyStarted"
            else:
                # Generate the ships
                game.start_game()

                status_code = 200
                response = f"Ships created, and game {game_name} started"

        return JsonResponse(response, safe=False, status=status_code)

    except:
        status_code = 500
        return JsonResponse("Unknown error", safe=False, status=status_code)


def api_games_history(request, game_name):
    """Fetch the action history for a game"""

    try:
        # Fetch the game
        game = Game.objects.get(name=game_name)
        if not game:
            status_code = 404
            response = f"Could not find game {game_name}"
        else:
            response = game.list_actions_as_dicts()
            status_code = 200

        return JsonResponse(response, safe=False, status=status_code)

    except:
        status_code = 500
        return JsonResponse("Unknown error", safe=False, status=status_code)


def api_games_getships(request, game_name, player_name, secret):
    """Fetch the ships for a specific player in a specific game"""
    #TODO: Doesn't include the ship locations, so that needs to be fixed

    try:
        # Fetch the game
        game = Game.objects.get(name=game_name)
        if not game:
            status_code = 404
            response = f"Could not find game {game_name}"

        # Fetch the player
        player = Player.objects.get(name=player_name)
        if not player:
            status_code = 404
            response = f"Could not find player {player_name}"

        # Have we both?
        if game and player:
            # Check the secret
            if secret == player.get_secret():
                status_code = 200
                response = game.list_ships_by_player(player)
            else:
                status_code = 403
                response = f"Invalid secret for player {player_name}"

        return JsonResponse(response, safe=False, status=status_code)

    except:
        status_code = 500
        return JsonResponse(response, safe=False, status=status_code)


def api_games_getwinner(request, game_name):
    """Fetch a winner if there is one, or None otherwise"""

    try:
        # Fetch the game
        game = Game.objects.get(name=game_name)
        if not game:
            status_code = 404
            response = f"Could not find game {game_name}"
        else:
            status_code = 200
            response = game.get_winner()
            if response:
                # If it's not NULL, just get the name of the winner
                response = response.name

        return JsonResponse(response, safe=False, status=status_code)

    except:
        status_code = 500
        return JsonResponse(response, safe=False, status=status_code)


def api_strike(request, game_name, player_name, secret, x, y):
    """Fetch the ships for a specific player in a specific game"""

    try:
        # Fetch the game
        game = Game.objects.get(name=game_name)
        if not game:
            status_code = 404
            response = f"Could not find game {game_name}"

        # Fetch the player
        player = Player.objects.get(name=player_name)
        if not player:
            status_code = 404
            response = f"Could not find player {player_name}"

        # Have we both?
        if game and player:
            # Check the secret
            if secret == player.get_secret():
                status_code = 200
                # Get the potential action and return
                location = (int(x),int(y))
                # Get the text from the output
                response = game.strike(player, location).result
            else:
                status_code = 403
                response = f"Invalid secret for player {player_name}"

        return JsonResponse(response, safe=False, status=status_code)

    except PermissionDenied as e:
        # The model strike code can raise exceptions, for instance, if it isn't the players turn.
        # Return the exception as a string so the client can deduce the reason
        status_code = 403
        return JsonResponse(str(e), safe=False, status=status_code)

    except:
        # Anything else should be supressed for security reasons
        status_code = 500
        return JsonResponse(f"Unknown error: Strike game {game_name}, player {player_name}, location ({x}, {y})"
                            , safe=False, status=status_code)

