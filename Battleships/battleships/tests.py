from django.test import TestCase

from .models import Action
from .models import Game
from .models import Location
from .models import Player
from .models import Ship

class GameStrikeTestCase(TestCase):
    """Test the mechanisms for ship strikes"""
    def setUp(self):

        # Create a game
        game = Game.objects.create(name="test_game")

        # Create and add players
        p1 = Player.objects.create(name="player1")
        p2 = Player.objects.create(name="player2")
        p3 = Player.objects.create(name="player3")

        game.players.add(p1)
        game.players.add(p2)
        game.players.add(p3)

        # Create a single ship
        game._create_ship_check('horizontal', p1, (3, 3), 3, name="Enterprise")


    def test_count_locations(self):
        # Test that the ship locations were added, there should be 3
        game = Game.objects.get(name="test_game")
        locations = Location.objects.all().filter(game=game)
        ship = Ship.objects.get(name="Enterprise")

        # The game should only have three locations stored so far
        self.assertEqual(3, Location.objects.all().filter(game=game).count())

        # Make sure the locations belong to the ship
        self.assertEqual(3, ship.locations.all().count())


    def test_check_for_hit_failure(self):
        # Test that the check_if_hit model logic
        game = Game.objects.get(name="test_game")

        ship = game.check_for_hit((1,1))
        self.assertIsNone(ship)


    def test_check_for_hit_success(self):
        # Test that the check_if_hit model logic
        game = Game.objects.get(name="test_game")

        ship = game.check_for_hit((3,3))
        self.assertIsInstance(ship, Ship)


    def test_strike_failure(self):
        """Test a valid strike"""

        game = Game.objects.get(name="test_game")
        p1 = Player.objects.get(name="player1")

        action = game.strike(p1, (1,1))
        self.assertIsInstance(action, Action)
        self.assertEqual(1, Ship.objects.all().filter(game=game).count())


    def test_strike_success(self):
        """Test a valid strike"""

        game = Game.objects.get(name="test_game")
        p1 = Player.objects.get(name="player1")

        action = game.strike(p1, (3,3))
        # We should have got a valid action
        self.assertIsInstance(action, Action)
        # There should be no more ships now!
        self.assertEqual(0, Ship.objects.all().filter(game=game).count())


    def test_turn_by_turn_success(self):
        """Check players taking it in turn works correctly"""

        game = Game.objects.get(name="test_game")
        p1 = Player.objects.get(name="player1")
        p2 = Player.objects.get(name="player2")
        p3 = Player.objects.get(name="player3")

        # Player 1 turn one
        action = game.strike(p1, (1,1))
        self.assertIsInstance(action, Action)
        self.assertEqual(1, Ship.objects.all().filter(game=game).count())

        # Player 2 turn one
        action = game.strike(p2, (2,1))
        self.assertIsInstance(action, Action)
        self.assertEqual(1, Ship.objects.all().filter(game=game).count())

        # Player 3 turn one
        action = game.strike(p3, (3,1))
        self.assertIsInstance(action, Action)
        self.assertEqual(1, Ship.objects.all().filter(game=game).count())

        # Player 1 turn two
        action = game.strike(p1, (4,1))
        self.assertIsInstance(action, Action)
        self.assertEqual(1, Ship.objects.all().filter(game=game).count())


    def test_turn_by_turn_failure(self):
        """Check players taking it in turn works correctly"""

        game = Game.objects.get(name="test_game")
        p1 = Player.objects.get(name="player1")
        p2 = Player.objects.get(name="player2")
        p3 = Player.objects.get(name="player3")

        # Player 1 turn one
        action = game.strike(p1, (1,1))
        self.assertIsInstance(action, Action)
        self.assertEqual(1, Ship.objects.all().filter(game=game).count())

        # Player 2 turn one
        action = game.strike(p2, (2,1))
        self.assertIsInstance(action, Action)
        self.assertEqual(1, Ship.objects.all().filter(game=game).count())

        # Player 1 tries to take turn two - should not be allowed
        action = game.strike(p1, (3,1))
        self.assertIsNone(action)
        self.assertEqual(1, Ship.objects.all().filter(game=game).count())


class ShipCreationTestCase(TestCase):
    """Test the mechanisms for ship creation"""
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


