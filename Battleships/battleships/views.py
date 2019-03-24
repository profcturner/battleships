from django.shortcuts import render
from django.http import HttpResponse
from .models import Game


# Create your views here.
def homepage(request):
    games = Game.objects.all()
    return render(request, 'homepage.html', {'games': games})

def game_players(request, pk):
    game = Game.objects.get(pk=pk)
    return render(request, 'game_players.html', {'game' : game})
