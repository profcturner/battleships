# battleships

A simple Battleships game server for educational use. The server is written in Python (3) Django, and provides a very basic API with text and data encoded in JSON. It is intended to need nothing other than simple HTTP GET requests.

The idea is to expose a simple API for students to write clients against - this is initially aimed at my first year students learning Python, but there's no reason why the server could not provide an API for Android or any other platform. The API is deliberately naive, but the plan is to make the server more robust with rate limiting.

Students may wish to read about HTTP response codes: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes and about Python and JSON https://www.w3schools.com/python/python_json.asp.

The code is written for Python Django, and needs Python 3.6 or higher.

## API 1.0

In version 1.0 of the API, all URLs are prefixed with *api/1.0/*. URLs are shown below, where data to be passed is shown _like so_. And a brief description of the function shown. More details to be added. All data is serialised using JSON. It is possible to use the response status code in many places to determine if the request is successful.

While this document records the current API, it may still have bugs and need tweaks, and should be considered experimental.

| URL                                      | Function                                       |
| -----------------------------------------| ---------------------------------------------- |
| players/index/                           | List current registered players                |
| players/register/_name_/                 | Register a player with text name               |
| players/delete/_name_/_secret_           | Delete a player                                |
| games/index/                             | List current registered games                  |
| games/register/_name_/                   | Create a new game                              |
| games/delete/_name_/_secret_/            | Delete a game                                  |
| games/addplayer/_game_/_name_/           | Add a player to a game                         |
| games/start/_game_/                      | Generate ships and start game                  |
| games/history/_game_/                    | Show actions so far in game                    |
| games/getships/_game_/_player_/_secret_/ | Get all the ships for a given player in a game |
| games/getwinner/_game_/                  | Returns a winner, used to detect game over     |
| strike/_game_/_player_/_(x,y)_/_secret_/ | Attempt to hit a grid square                   |

### players/index/

This API call provides a list of players registered on the server.

| outcome   | status code | content                                                         |
|-----------|-------------|-----------------------------------------------------------------|
| *success* | 200         | A list of dict objects for players, formatted name: player_name |
| *failure* | 500         | Unknown server error                                            |

### players/register/_name_/

This API call allows a new player to be added to the server. The player name is specified as above in _name_ and should be alphanumeric characters only and not include spaces. If successful, a secret will be generated and returned. This _secret_ is used in several other API calls to authenticate the player, and so should be recorded by the client.

| outcome   | status code | content                                                         |
|-----------|-------------|-----------------------------------------------------------------|
| *success* | 200         | The _secret_ code for that player, which should be recorded     |
| *failure* | 403         | Forbidden, which may be due to the name being in use            |

### players/delete/_name_/_secret_/

This API call deletes a player from the server. Note this will also delete ships belonging to the player, and actions from history, and so should be done with care. The player name is specified as above in _name_ and the _secret_ used in registering the player.

| outcome   | status code | content                                                         |
|-----------|-------------|-----------------------------------------------------------------|
| *success* | 200         | Player _name_ deleted                                           |
| *failure* | 403         | Invalid secret                                                  |
| *failure* | 404         | Could not find player _name_                                    |
| *failure* | 500         | Unknown server error                                            |

### games/index/

This API call provides a list of gamers registered on the server.

| outcome   | status code | content                                                         |
|-----------|-------------|-----------------------------------------------------------------|
| *success* | 200         | A list of dict objects for games, formatted name: game_name     |
| *failure* | 500         | Unknown server error                                            |

### games/register/_name_/

This API call allows a new game to be added to the server. The game name is specified as above in _name_ and should be alphanumeric characters only and not include spaces. If successful, a secret will be generated and returned. This _secret_ is used in several other API calls to authenticate the creator of the game, and so should be recorded by the client. Note that no ships are created until players are added and the game started.

| outcome   | status code | content                                                         |
|-----------|-------------|-----------------------------------------------------------------|
| *success* | 200         | The _secret_ code for that game, which should be recorded       |
| *failure* | 403         | Forbidden, which may be due to the name being in use            |

### games/delete/_name_/_secret_/

This API call deletes a game from the server. Note this will also delete ships belonging to the game, and actions from history, and so should be done with care. The game name is specified as above in _name_ and the _secret_ used in registering the game.

| outcome   | status code | content                                                         |
|-----------|-------------|-----------------------------------------------------------------|
| *success* | 200         | Game _name_ deleted                                             |
| *failure* | 403         | Invalid secret                                                  |
| *failure* | 404         | Could not find game _name_                                      |
| *failure* | 500         | Unknown server error                                            |

### games/addplayer/_game_/_player_/

This API call adds an existing player to an existing game.  The name of the _game_ and _player_ should be entered as above. The API will not allow players to be added once the game is started and ships exist.

| outcome   | status code | content                                                         |
|-----------|-------------|-----------------------------------------------------------------|
| *success* | 200         | Player _player_ added to game _game_                            |
| *failure* | 403         | Player _player_ is already in game _game_                       |
| *failure* | 403         | Game already started                                            |
| *failure* | 404         | Could not find game _game_                                      |
| *failure* | 404         | Could not find player _player_                                  |
| *failure* | 500         | Unknown server error                                            |

### games/start/_game_/

This API call generates random ships for all players currently registered in the game. Calls when ships already exist will be rejected.

| outcome   | status code | content                                                         |
|-----------|-------------|-----------------------------------------------------------------|
| *success* | 200         | Ships created and game _game_ started                           |
| *failure* | 403         | Game already started                                            |
| *failure* | 404         | Could not find game _game_                                      |
| *failure* | 500         | Unknown server error                                            |

### games/history/_game_/

This API call returns all the actions recorded for a game so far. If successful, a list of dict objects is returns, which contains:

"game" : _game_;

"player" : _player_;

"location" : a tuples of the form (x,y) with the location of an attempted strike;

"result" : the result text as provided by the strike API call;

"created" : the datestamp of the action.

| outcome   | status code | content                                                         |
|-----------|-------------|-----------------------------------------------------------------|
| *success* | 200         | A list of dict objects for an action as above                   |
| *failure* | 404         | Could not find game _game_                                      |
| *failure* | 500         | Unknown server error                                            |

### games/getships/_game_/_player_/_secret_/ 

This API call returns all the (surviving) ships within a _game_ for a given _player_. Because this is sensitive game information, the player _secret_ is required. This call can be used after the game start to determine where the ships have been generated, or during a game to check which ships are surviving. Each ship is stored in a dict with the following data:

"name" : the name of the ship;

"locations" : a list oftuples of the form (x,y) showing the grid squares the ship occupies.

| outcome   | status code | content                                                         |
|-----------|-------------|-----------------------------------------------------------------|
| *success* | 200         | A list of dict objects for ships as above                       |
| *failure* | 403         | Invalid secret for player _player_                              |
| *failure* | 404         | Could not find game _game_                                      |
| *failure* | 404         | Could not find player _player_                                  |
| *failure* | 500         | Unknown server error                                            |

### games/getwinner/_game_/ 

This API call is used to determine if the game has a winner, and if so who it is. It can be used to detect if the game is over.

| outcome   | status code | content                                                         |
|-----------|-------------|-----------------------------------------------------------------|
| *success* | 200         | null if there is no player                                      |
| *success* | 200         | _player_ if there is a winner                                   |
| *failure* | 404         | Could not find game _game_                                      |
| *failure* | 500         | Unknown server error                                            |

### strike/_game_/_player_/_location_/_secret_/ 

This API call allows players to attempt to hit each other's ships. It requires the _game_ and _player_ names, the player _secret_ to authenticate the player, and a location which is a tuple of the form (x,y).

From a web request point of view, hits and misses are considered successful.

The server enforces a turn based system. In any given turn any player can act in any order. However, the system will prevent a player taking a further turn until their peers have caught up. The server will not allow strikes until ships have been created, and prohibits players not added into a game being allowed to strike.

There is no protection against friendly fire.

| outcome   | status code | content                                                         |
|-----------|-------------|-----------------------------------------------------------------|
| *success* | 200         | miss:                                                           |
| *success* | 200         | hit: ship _ship_ belonging to _player_ has been sunk.           |
| *failure* | 403         | Invalid secret for player _player_                              |
| *failure* | 403         | NotInGame                                                       |
| *failure* | 403         | NoShipsInGame                                                   |
| *failure* | 403         | NotYourTurn                                                     |
| *failure* | 404         | Could not find game _game_                                      |
| *failure* | 404         | Could not find player _player_                                  |
| *failure* | 500         | Unknown server error                                            |

## HTML views

There is currently a single html web page provided to help admins, and potentially players and students.

### <BASE_URL>/view_game/_game_/_player_/_secret_/

Note that this is *not* in the API tree, this URL goes straight onto your base url for the server.

Superusers who have logged in can use this to view any game and can omit the _player_ and _secret_ variables. If a superuser uses the _player_ variable they do not have to use the secret, in case they want to demonstrate something to a student.

Normal users must specify all parts and only that player's ships in the game will be displayed.

## Installing This Software

This package requires Python 3.6+ and Django. Installing these on a production server isn't so hard, but beyond the scope of this documentation. Google is your friend here.

To install in a development environment, again you'll need Python and Django (and maybe git or GitHub to easily clone or fork the code). The details vary by OS and circumstance, but you may want to Google using pip or pip3 to install Django once you have Python. You may also want to explore the pros and cons of using a venv.

## Creating the Database

You may wish to tweak the database server, but you can create the initial database with

```
python3 manage.py migrate
```

## Creating a Superuser

Once installed, you probably want to create a superuser, find the directory containing manage.py and use this command.

```
python3 manage.py createsuperuser
```

will allow you to create a superuser account.

```
python3 manage.py runserver
```

will allow you to run a test server instance to play with.

You only need a superuser to manipulate the database directly, but it also allows an admin view of games that can be useful. For instance, in the main games list the games are hyperlinked, but the admin view is protected for obvious reasons (it shows all ship positions).

Go to the /admin/ directory of your project to get a login prompt. Once logged in go back to the main directory. Now you will be able to view games that are linked with more details.

## Django Admin pages

Superusers can access the Django admin interface at <BASE_URL>/admin/ which can allow you to delete and create items as needed within the database without using the API. Note that this bypasses any API logic.



