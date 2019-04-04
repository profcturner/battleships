from django.contrib import admin

# Register your models here.

from django.contrib import admin

# Importing some extra stuff to allow us to extend User

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.

# Import given models

from .models import Action
from .models import Game
from .models import GameSecret
from .models import Player
from .models import PlayerSecret
from .models import Ship


# Some code to augment the admin views in some cases

class ActionAdmin(admin.ModelAdmin):
    list_display = (
        'game', 'player', 'result', 'location', 'created'
    )
    list_filter = ('game',)

class GameAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'maximum_x', 'maximum_y', 'ships_per_person', 'created', 'modified'
    )

class ShipAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'game', 'player'
    )
    list_filter = ('game',)

class PlayerAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'created', 'modified'
    )

class GameSecretAdmin(admin.ModelAdmin):
    list_display = ('game', 'secret')

class PlayerSecretAdmin(admin.ModelAdmin):
    list_display = ('player', 'secret')


admin.site.register(Action, ActionAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(GameSecret, GameSecretAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(PlayerSecret, PlayerSecretAdmin)
admin.site.register(Ship, ShipAdmin)

