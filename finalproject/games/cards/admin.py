from django.contrib import admin

from .models import User, TwoPlayerGame, TicTacToe

# Register your models here.

admin.site.register(User)
admin.site.register(TicTacToe)
