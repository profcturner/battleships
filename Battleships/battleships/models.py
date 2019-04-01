from django.db import models
from random import choice, randint

class Player(models.Model):
    """A very disposable player class. At some point we will probably link these players to Django users, but
    that will complicate API design for students, so starting here.

    name        A unique text name for the player
    created     When the player was created
    modified    When the player was last modified"""

    name = models.CharField(max_length=50, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


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
    maximum_x = models.IntegerField(default=30)
    maximum_y = models.IntegerField(default=30)
    ships_per_person = models.IntegerField(default=3)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    players = models.ManyToManyField(Player)
    
    
    def _create_ship_check(self, orientation, player, start_location, ship_length, name="Unnamed"):
        """Try to create a horizontal ship from a certain location to the right

        orientation     One of "horizontal", "vertical" or "diagonal" with which to attempt to build the ship
        player          The player who will own any created ship
        start_location  A tuple (x,y) of the start position
        ship_length     We will try to occupy this many cells to the right of the start_location
        name            A name for any successfully created ship

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
        """A function to automatically generate ships for the players"""

        # Get all existing ships
        ships = Ship.objects.all().filter(game=self)

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
        """Checks for any hit, returns the ship for any hit, or None otherwise"""

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
        location    the location to strike

        returns an Action is the strike was a valid attempt or None otherwise
        """

        # If the player isn't in the game, stop now
        if player not in self.players.all():
            return None

        # If there are no ships, stop now
        if not Ship.objects.all().filter(game=self).count():
            return None

        # Get actions to date
        all_actions = Action.objects.all().filter(game=self)

        # If the current player is already a move ahead of anyone else then we should disallow this attempt
        number_of_player_actions = all_actions.filter(player=player).count()
        for p in self.players.all():
            if number_of_player_actions > all_actions.filter(player=p).count():
                return None

        # Check for any hit
        ship = self.check_for_hit(location)
        if ship:
            # A ship was hit!
            result = f"The ship {ship.name} belonging to {ship.player.name} was sunk!"
            # Delete the ship from the database
            ship.delete()
        else:
            # It was a miss!
            result = f"That was a miss."

        (x, y) = location
        location_object = Location.objects.create(x=x, y=y, game=self)
        action = Action.objects.create(game=self, player=player, location=location_object, result=result)

        return action


    def number_of_ships(self, player):
        """Return the number of active ships for a given player"""
        return len(Ship.objects.all().filter(game=self).filter(player=player))


class Location(models.Model):
    """A grid location. Mainly used to record ship cells, and strike attempts.

    x       The x location
    y       The y location
    game    The game with this this is associated (for ease of cleanup)
    """

    x = models.IntegerField()
    y = models.IntegerField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)


class Ship(models.Model):
    """An individual ship within the game

    name        A name for the ship
    game        The game in which the ship exists
    player      The Player who owns the ship
    locations   The grid cells occupied by the ship"""


    name = models.CharField(max_length=50)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    locations = models.ManyToManyField(Location)

    def check_for_hit(self, location):
        """Checks if the ship is on a given location and returns True or False"""

        (x, y) = location
        # Check if the passed in location is in the list of ship locations
        for location in self.locations.all():
            if x == location.x and y == location.y:
                return True

        return False



class Action(models.Model):
    """Records actions within a given game

    game      The Game within which the action occurred
    player    The Player who took the action
    location  The location of the attempted hit
    result    A short text description of the outcome"""

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    result = models.CharField(max_length=50)
    
    
