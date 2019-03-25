from django.test import TestCase
from django.urls import reverse
from django.urls import resolve
from .views import homepage, game_players
from .models import Game


# Create your tests here.
class HomePageTests(TestCase):

    def test_home_view_status_code(self):
        url = reverse('homepage')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)


    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, homepage)

class GamePlayersTests(TestCase):
    def setUp(self):
        Game.objects.create(name='Test')

    def test_game_players_view_success_status_code(self):
        url = reverse('game_players', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_game_players_view_not_found_status_code(self):
        url = reverse('game_players', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    # This test is referring to an entity (board_topics) that doesn't exist
    #def test_game_players_url_resolves_board_topics_view(self):
    #    view = resolve('/games/1/')
    #    self.assertEquals(view.func, board_topics)
