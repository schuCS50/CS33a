
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('newgame', views.newGame, name='newgame'),
    path('user/<str:username>', views.userGames, name="userGames"),
    path('tictactoe/<int:game_id>', views.tictactoe, name='tictactoe'),
    path('tictactoe/game/<int:game_id>',
         views.tictactoe_api,
         name='tictactoe_api'),
    path('chat', views.chat, name='chat'),
    path('<str:room_name>/', views.room, name='room'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
