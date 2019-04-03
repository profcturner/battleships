# battleships

A simple Battleships game server for educational use. The server is written in Python (3) Django, and provides a very basic API with text and data encoded in JSON. It is intended to need nothing other than simple HTTP GET requests.

The idea is to expose a simple API for students to write clients against - this is initially aimed at my first year students learning Python, but there's no reason why the server could not provide an API for Android or any other platform. The API is deliberately naive, but the plan is to make the server more robust with rate limiting.

## API 1.0

In version 1.0 of the API, all URLs are prefixed with *api/1.0/*. URLs are shown below, where data to be passed is shown _like so_. And a brief description of the function shown. More details to be added.

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
