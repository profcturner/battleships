# battleships

A simple Battleships game server for educational use.

The idea is to expose a simple API for students to write clients against.

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
| strike/_game_/_player_/_(x,y)_/_secret_/ | Attempt to hit a grid square                   |
