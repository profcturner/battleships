# Battleships models.py

# From standard Python we will need some functions for randomness
from random import choice, randint, shuffle

# And strings
import string

# From Django we need model code
from django.db import models

# And we will sometimes raise exceptions
from django.core.exceptions import PermissionDenied


class Player(models.Model):
    """A very disposable player class. At some point we will probably link these players to Django users, but
    that will complicate API design for students, so starting here.

    name        A unique text name for the player
    created     When the player was created
    modified    When the player was last modified"""

    name = models.CharField(max_length=50, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    @staticmethod
    def list_players_as_dicts():
        """A list of players as dicts to be more easily serialisable

        Currently contains only names

        """

        player_list = []
        players = Player.objects.all()
        for player in players:
            player_dict = {
                "name" : player.name
            }
            player_list.append(player_dict)

        return player_list


    def create_secret(self):
        """Set a secret code for the current game and return that secret"""

        # Alpha Numeric six digit string
        alpha_numeric = string.ascii_letters + string.digits
        secret = ''.join(choice(alpha_numeric) for i in range(6))

        # Nuke any existing secrets
        PlayerSecret.objects.all().filter(player=self).delete()
        # Add the new secret
        PlayerSecret.objects.create(player=self, secret=secret)

        return secret

    def get_secret(self):
        """Fetch any secret and return it, if none exists return None"""

        player_secrets = PlayerSecret.objects.all().filter(player=self)

        if not player_secrets.count():
            # There's no secret
            return None
        else:
            # Return the secret, there shouldn't be more than one, but return the first
            return player_secrets[0].secret

    def get_colour(self):
        """This will allocate a consistent colour to players based on the name.
        This is used by the basic internal views to show consistent colours for given players
        """

        colours = [
            'indianred',
            'lightsalmon',
            'darkred',
            'pink',
            'hotpink',
            'orange',
            'gold',
            'khaki',
            'plum',
            'magenta',
            'blueviolet',
            'slateblue',
            'lime',
            'seagreen',
            'teal',
            'aqua',
            'tan',
            'brown',
        ]

        # Return a colour from the above list we get from a remainder when we divide the
        # unique hash by the number of colours.
        return colours[hash(self.name) % len(colours)]


    def __str__(self):
        return self.name


    class Meta:
        ordering = ['name']


class Game(models.Model):
    """A specific game between 2 or more players

    name                The name of the game
    maximum_x           The largest possible x value
    maximum_y           The largest possible y value
    ships_per_person    The number of ships to generate for each player
    created             When the game was created
    modified            When the game was last modified / accessed
    players             The Players in the game
    """

    name = models.CharField(max_length=50, unique=True)
    maximum_x = models.IntegerField(default=15)
    maximum_y = models.IntegerField(default=15)
    ships_per_person = models.IntegerField(default=3)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    players = models.ManyToManyField(Player)


    @staticmethod
    def list_games_as_dicts():
        """A list of players as dicts to be more easily serialisable

        Currently contains only names

        """

        game_list = []
        games = Game.objects.all()
        for game in games:
            game_dict = {
                "name" : game.name
            }
            game_list.append(game_dict)

        return game_list


    def create_secret(self):
        """Set a secret code for the current game and return that secret"""

        # Alpha Numeric six digit string
        alpha_numeric = string.ascii_letters + string.digits
        secret = ''.join(choice(alpha_numeric) for i in range(6))

        # Nuke any existing secrets
        GameSecret.objects.all().filter(game=self).delete()
        # Add the new secret
        GameSecret.objects.create(game=self, secret=secret)

        return secret


    def get_secret(self):
        """Fetch any secret and return it, if none exists return None"""

        game_secrets = GameSecret.objects.all().filter(game=self)

        if not game_secrets.count():
            # There's no secret
            return None
        else:
            # Return the secret, there shouldn't be more than one, but return the first
            return game_secrets[0].secret


    def start_game(self):
        """Generate ships for all players in the game"""

        for player in self.players.all():
            for x in range(0, self.ships_per_person):
                self.create_ship(player)


    def _create_ship_check(self, orientation, player, start_location, ship_length, name=None):
        """Try to create a horizontal ship from a certain location to the right

        orientation     One of "horizontal", "vertical" or "diagonal" with which to attempt to build the ship
        player          The player who will own any created ship
        start_location  A tuple (x,y) of the start position
        ship_length     We will try to occupy this many cells to the right of the start_location
        name            A name for any successfully created ship, None for a random choice

        returns a Ship that has been added to the database, or None otherwise
        """

        # If the orientiation is void, return None
        # TODO: Consider raising an error perhaps?
        if orientation not in ['horizontal', 'vertical', 'diagonal']:
            return None

        # Get the start coordinates from the tuple location
        (startx, starty) = start_location

        # Make a list of the potential locations the ship would occupy
        possible_locations = []
        if orientation == 'horizontal':
            # Head to the right from the start location
            if startx + ship_length > self.maximum_x:
                # Not enough room
                return None
            for x in range(0, ship_length):
                possible_locations.append((startx+x,starty))
        if orientation == 'vertical':
            # Head above the start location (if above is larger y)
            if starty + ship_length > self.maximum_y:
                # Not enough room
                return None
            for y in range(0, ship_length):
                possible_locations.append((startx,starty+y))
        if orientation == 'diagonal':
            # Head to top right of start location
            if startx + ship_length > self.maximum_x or starty + ship_length > self.maximum_y:
                # Not enough room
                return None

            for xy in range(0, ship_length):
                possible_locations.append((startx+xy,starty+xy))

        # Check of any of these collide with existing ships
        for location in possible_locations:
            if self.check_for_hit((location)):
                # Already a ship there, we can't create a new one
                return None

        # We had no collisions, so the space must be free, create the new ship
        if not name:
            name = self.get_random_ship_name()
        ship = Ship.objects.create(name=name,
                            game=self,
                            player=player)

        # Save its locations, creating those in the Model layer
        for (x,y) in possible_locations:
            model_location = Location.objects.create(x=x,y=y,game=self)
            ship.locations.add(model_location)
        ship.save()

        return ship


    def create_ship(self, player, ship_length=3):
        """A function to automatically generate a random ship for a player

        player          the Player object who should get the ship
        ship_length     the number of locations the ship will occupy (3 by default)
        """

        # Pick an orientation
        orientation = choice(['horizontal', 'vertical', 'diagonal'])

        # Maintain a list of tuples of possible starting points
        start_locations_tried = list()

        # Keep going till we have created the ship, or exhausted all possibilities
        while  (len(start_locations_tried) < (self.maximum_x * self.maximum_y)):
            # Pick a start location. This is naive at best
            startx = randint(1, self.maximum_x)
            starty = randint(1, self.maximum_y)

            if (startx, starty) in start_locations_tried:
                # This one is used, go around the block
                continue
            else:
                # Track this choice
                start_locations_tried.append((startx, starty))

            ship = self._create_ship_check(orientation, player, (startx, starty), ship_length)
            if ship:
                return ship

        # Oops, we just couldn't fit in the ship
        return None


    def check_for_hit(self, location):
        """Checks for any hit, returns the ship for any hit, or None otherwise

        location    a location tuple (x,y) to check for a hit
        """

        # Get all existing ships in this game
        ships = Ship.objects.all().filter(game=self)

        for ship in ships:
            if ship.check_for_hit(location):
                return ship

        # Nothing?
        return None


    def strike(self, player, location):
        """Process an attempted strike from a specified player

        player      the player to take the action
        location    the location to strike as a tuple (x,y)

        returns an Action is the strike was a valid attempt or an error string otherwise
        """

        # If the player isn't in the game, stop now
        if player not in self.players.all():
            raise PermissionDenied("NotInGame")

        # If there are no ships, stop now
        if not Ship.objects.all().filter(game=self).count():
            raise PermissionDenied("NoShipsInGame")

        # Get actions to date
        all_actions = Action.objects.all().filter(game=self)

        # If the current player is already a move ahead of anyone else then we should disallow this attempt
        number_of_player_actions = all_actions.filter(player=player).count()
        for p in self.players.all():
            if number_of_player_actions > all_actions.filter(player=p).count():
                raise PermissionDenied("NotYourTurn")

        # Check for any hit
        ship = self.check_for_hit(location)
        if ship:
            # A ship was hit!
            result = "hit: ship {} belonging to {} was sunk.".format(ship.name, ship.player.name)
            # Delete the ship from the database
            ship.delete()
        else:
            # It was a miss!
            result = "miss:"

        # Our input location is a tuple, but we need to convert it to a Location object
        (x, y) = location
        location_object = Location.objects.create(x=x, y=y, game=self)
        action = Action.objects.create(game=self, player=player, location=location_object, result=result)

        # Save both game and player to force modified timestamp update
        self.save()
        player.save()

        return action


    def number_of_ships(self, player=None):
        """Return the number of active ships

        player      if supplied, only the ships for this player are counted, if None, all are counted
        """

        ships = Ship.objects.all().filter(game=self)
        if player:
            ships = ships.filter(player=player)

        return ships.count()


    def list_actions_as_dicts(self):
        """Return all the actions associated with the game as a list of dicts"""

        action_list = []
        actions = Action.objects.all().filter(game=self).order_by("created")
        for action in actions:
            action_dict = {
                "game" : action.game.name,
                "player" : action.player.name,
                "location" : ((action.location.x, action.location.y)),
                "result" : action.result,
                "created" : action.created
            }
            action_list.append(action_dict)

        return action_list


    def list_ships_by_player(self, player):
        """Return a list of ship objections as dicts for a given player"""

        ships_list = []
        ships = Ship.objects.all().filter(game=self).filter(player=player)
        for ship in ships:
            ship_dict = {
                "name": ship.name,
                "locations": ship.get_locations_as_tuples()
            }
            ships_list.append(ship_dict)
        return ships_list


    def get_ships_by_player(self):
        """Get the list of active ships by player

        returns a dict keyed by player, and with value the QuerySet of ships
        """

        ships_by_player = dict()
        for player in self.players.all():
            ships_by_player[player] = Ship.objects.all().filter(game=self).filter(player=player)

        return ships_by_player


    def get_winner(self):
        """Check for any winner, returns a Player if so, or None otherwise"""

        # TODO: This algorithm feels horribly convoluted...
        ships_by_player = self.get_ships_by_player()

        # If there are no players, give up now
        if not len(ships_by_player):
            return None

        # Make a simpler list of tuples, [(player, number of ships)]
        ship_numbers = []

        for player, ships in ships_by_player.items():
            ship_numbers.append((player, len(ships)))

        # Sort them by descending numbers of ships (winners first)
        ship_numbers = sorted(ship_numbers, key=lambda x: x[1], reverse=True)

        # Get the top ranked player - it will be the first in the list
        (top_player, top_player_ships) = ship_numbers[0]
        # If they have no ships, then nobody has any, and nobody wins (maybe no ships have yet been created)
        if not top_player_ships:
            return None

        # Ok, if anyone else has ships there is no winner yet, so return None
        for x in range(1, len(ship_numbers)):
            (player, player_ships) = ship_numbers[x]
            if player_ships:
                return None

        # Nobody else had ships and the top_player did so we have a winner
        return(top_player)


    def get_random_ship_name(self):
        """
        Returns a random ship name, with thanks to Ian M. Banks

        Feel free to add more
        https://en.wikipedia.org/wiki/List_of_spacecraft_in_the_Culture_series

        """

        names = [
            "Bora Horza Gobuchul",
            "Determinist",
            "Eschatologist",
            "Irregular Apocalypse",
            "No More Mr Nice Guy",
            "Profit Margin",
            "Nervous Energy",
            "Prosthetic Conscience",
            "Revisionist",
            "Trade Surplus",
            "The Ends Of Invention",
            "Clear Air Turbulence",
            "Little Rascal",
            "So Much For Subtlety",
            "Unfortunate Conflict Of Evidence",
            "Youthful Indiscretion",
            "Flexible Demeanour",
            "Just Read The Instructions",
            "Of Course I Still Love You",
            "Zealot",
            "Limiting Factor",
            "Gunboat Diplomat",
            "Kiss My Ass",
            "Prime Mover",
            "Screw Loose",
            "Bad for Business",
            "Ablation",
            "Arrested Development",
            "A Series Of Unlikely Explanations",
            "A Ship With A View",
            "Big Sexy Beast",
            "Boo!",
            "Cantankerous",
            "Credibility Problem",
            "Dramatic Exit",
            "Excuses and Accusations",
            "Death And Gravity",
            "Anticipation Of A New Lover's Arrival, The",
            "Ethics Gradient",
            "Honest Mistake",
            "Limivorous",
            "Uninvited Guest",
            "Use Psychology",
            "Yawning Angel",
            "Zero Gravitas",
            "Serious Callers Only",
            "Steely Glint",
            "Different Tan",
            "Problem Child",
            "Killing Time",
            "Quietly Confident",
            "Sleeper Service",
            "Mistake Not...",
        ]

        # Shuffle the list
        shuffle(names)

        # Try them in turn
        for name in names:
            # Already used?
            if not Ship.objects.all().filter(game=self).filter(name=name):
                # No... use this one
                return name

        # If we are here, then we ran out within the game
        return "Unavailable due to previous customer selection"


    def __str__(self):
        return self.name


    class Meta:
        ordering = ['name']


class Location(models.Model):
    """A grid location. Mainly used to record ship cells, and strike attempts.

    x       The x location
    y       The y location
    game    The game with this this is associated (for ease of cleanup)
    """

    x = models.IntegerField()
    y = models.IntegerField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        return "({}, {})".format(self.x, self.y)


class Ship(models.Model):
    """An individual ship within the game

    name        A name for the ship
    game        The game in which the ship exists
    player      The Player who owns the ship
    locations   The grid cells occupied by the ship as Location objects"""

    name = models.CharField(max_length=50)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    locations = models.ManyToManyField(Location)

    def check_for_hit(self, location):
        """Checks if the ship is on a given location and returns True or False"""

        # The input is a tuple, get the x and y coordinate
        (x, y) = location
        # Check if the passed in location is in the list of ship locations
        for location in self.locations.all():
            if x == location.x and y == location.y:
                return True

        return False

    def get_locations_as_tuples(self):
        """Return ship locations as a list of tuples (x,y)"""

        locations_as_tuples = []

        for location in self.locations.all():
            locations_as_tuples.append((location.x, location.y))

        return locations_as_tuples

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Action(models.Model):
    """Records actions within a given game

    game      The Game within which the action occurred
    player    The Player who took the action
    location  The location of the attempted hit
    result    A short text description of the outcome"""

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    result = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "game: {} result: {}".format(self.game, self.result)

    class Meta:
        ordering = ['created']


class PlayerSecret(models.Model):
    """Records secrets for players, in a separate table for safety

    The secret is created when players are created.

    player  The Player for whom the secret applies
    secret  A unique code used by the player for some API issues
    """

    player = models.OneToOneField(Player, on_delete=models.CASCADE)
    secret = models.CharField(max_length=20)

    def __str__(self):
        return "player: {}, secret: {}".format(self.player.name, self.secret)


class GameSecret(models.Model):
    """Records secrets for games, in a separate table for safety

    The secret is created when games are created.

    game    The Player for whom the secret applies
    secret  A unique code used by the player for some API issues
    """

    game = models.OneToOneField(Game, on_delete=models.CASCADE)
    secret = models.CharField(max_length=20)

    def __str__(self):
        return "game: {}, secret: {}".format(self.game.name, self.secret)
