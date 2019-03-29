from django.contrib import admin
from .models import Game, Player, Ship, Action, Location
# Register your models here.

admin.site.register(Game)
admin.site.register(Player)
admin.site.register(Ship)
admin.site.register(Action)
admin.site.register(Location)
