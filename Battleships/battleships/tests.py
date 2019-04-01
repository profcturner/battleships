from django.test import TestCase

from .models import Game
from .models import Player
from .models import Ship

class ShipCreationTestCase(TestCase):
    def setUp(self):

        Game.objects.create(name="test_game")

        Player.objects.create(name="player1")
        Player.objects.create(name="player2")
        Player.objects.create(name="player3")


    def test_horizontal_placement(self):
        """Attempt to create a ship horizontally"""

        game = Game.objects.get(name="test_game")
        p1 = Player.objects.get(name="player1")

        # There is room for this ship, so it should succeed
        ship = game._create_ship_check('horizontal', p1, (3,3), 3)
        self.assertIsInstance(ship, Ship)

        # There is no room for this ship so it should fail
        ship = game._create_ship_check('horizontal', p1, (29,3), 3)
        self.assertIsNone(ship)


    def test_vertical_placement(self):
        """Attempt to create a ship vertically"""

        game = Game.objects.get(name="test_game")
        p1 = Player.objects.get(name="player1")

        # There is room for this ship, so it should succeed
        ship = game._create_ship_check('vertical', p1, (3,3), 3)
        self.assertIsInstance(ship, Ship)

        # There is no room for this ship so it should fail
        ship = game._create_ship_check('vertical', p1, (3,29), 3)
        self.assertIsNone(ship)


    def test_diagonal_placement(self):
        """Attempt to create a ship horizontally"""

        game = Game.objects.get(name="test_game")
        p1 = Player.objects.get(name="player1")

        # There is room for this ship, so it should succeed
        ship = game._create_ship_check('diagonal', p1, (3,3), 3)
        self.assertIsInstance(ship, Ship)

        # There is no room for this ship so it should fail
        ship = game._create_ship_check('diagonal', p1, (29,3), 3)
        self.assertIsNone(ship)

        # There is no room for this ship so it should fail
        ship = game._create_ship_check('diagonal', p1, (3,29), 3)
        self.assertIsNone(ship)


    def test_create_ships(self):
        """This creates a game and tests random ship generation for three ships for each of three players"""

        game = Game.objects.get(name="test_game")
        p1 = Player.objects.get(name="player1")
        p2 = Player.objects.get(name="player2")
        p3 = Player.objects.get(name="player3")

        for player in [p1, p2, p3]:
            # Create 3 ships for player
            for x in range(0, game.ships_per_person):
                game.create_ship(player)

            # Check that was successful, i.e. that all ships were added to the database
            self.assertEqual(game.ships_per_person, game.number_of_ships(player))


