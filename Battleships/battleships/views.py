from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Game


# Create your views here.
def homepage(request):
    games = Game.objects.all()
    return render(request, 'homepage.html', {'games': games})

def game_players(request, pk):
    # We need to clear signal 404 if we don't get the match, not just an uncaught error
    game = get_object_or_404(Game, pk=pk)
    return render(request, 'game_players.html', {'game' : game})
