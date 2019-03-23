from django.db import models
from random import randint



class Player(models.Model):
    """A very disposable player class. At some point we will probably link these players to Django users, but
    that will complicate API design for students, so starting here.

    name        A unique text name for the player
    created     When the player was created
    modified    When the player was last modified"""

    name = models.CharField(max_length=50, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



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


    def __str__(self):
        return self.name

        
    def create_ship(self, player, ship_length=3):
        """A function to automatically generate ships for the players"""

        # Get all existing ships
        ships = Ship.objects.all().filter(game=self)

        # Pick an orientation
        # orientation 1 = horizonal ship, 2 = vertical ship, 3 = diagonal
        orientation = randint(1,3)

        # Maintain a list of tuples of possible starting points
        start_locations_tried = list()
        done = False

        # Keep going till we have created the ship, or exhausted all possibilities
        while not done and len(start_locations_tried < (maximum_x * maximum_y)):
            # Pick a start location. This is naive at best
            startx = randint(1, maximum_x)
            starty = randint(1, maximum_y)

            if (startx, starty) in start_locations_tried:
                # This one is used, go around the block
                continue
            else:
                # Track this choice
                start_locations_tried.append((startx, starty))

            #for x in range(0, ship_length):
                #if orientation == 1:


    def number_of_ships(self, player):
        """Return the number of active ships for a given player"""
        return len(Ships.objects.all().filter(game=self).filter(player=player))


class Location(models.Model):
    """A grid location. Mainly used to record ship cells, and strike attempts.

    x    The x location
    y    The y location
    """

    x = models.IntegerField()
    y = models.IntegerField()



class Ship(models.Model):
    """An individual ship within the game

    name        A name for the ship
    game        The game in which the ship exists
    player      The Player who owns the ship
    locations   The grid cells occupied by the ship"""


    name = models.CharField(max_length=50)
    #Set the on_delete actions to be CASCADE as my virtual env was saying the are not nullable
    #and Cascade seems to achieve what we want unless I misunderstood
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)





class Action(models.Model):
    """Records actions within a given game

    game      The Game within which the action occurred
    player    The Player who took the action
    location  The location of the attempted hit
    result    A short text description of the outcome"""

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    result = models.CharField(max_length=50)
