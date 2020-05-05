from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Count, Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse


import json
import time
from .models import User, TicTacToe

# Create your views here.


# Home view for all games
def index(request):
    games = TicTacToe.objects.all().order_by("-createdTimestamp")
    return render(request, 'cards/index.html', {
        'games': games,
        'allGames': True
    })


# View for a given user's games
def userGames(request, username):
    user = User.objects.get(username=username)
    games = TicTacToe.objects.filter(
        Q(player1=user) | Q(player2=user)
    ).order_by("-createdTimestamp")
    return render(request, 'cards/index.html', {
        'games': games,
        'allGames': False
    })


# View for new game creation
def newGame(request):
    # If request is POST, create new game
    if request.method == "POST":
        p2 = User.objects.get(pk=request.POST['player2'])
        game = TicTacToe(player1=request.user, player2=p2)
        game.save()
        return HttpResponseRedirect(reverse("tictactoe", args=[game.id]))

    # Otherwise render page
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'cards/newgame.html', {
        'users': users
    })


# View to render game page
def tictactoe(request, game_id):
    game = TicTacToe.objects.get(pk=game_id)
    return render(request, 'cards/tictactoe.html', {
        'game': game,
        'player': game.player1 == request.user or game.player2 == request.user
    })


# Helper view to handle gameplay requests
def tictactoe_api(request, game_id):
    game = TicTacToe.objects.get(pk=game_id)

    # With put request, update game appropriately
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get('location') is not None:
            cellId = data['location'][4]
            user = User.objects.get(username=data['user'])
            exec(f'game.cell{cellId}=user')
            game.save()
            return HttpResponse(status=204)
        if data.get("won") is not None:
            user = User.objects.get(username=data['user'])
            game.winner = user
            game.save()
            return HttpResponse(status=204)
    # Otherwise return game
    else:
        return JsonResponse(game.serialize(), safe=False)


# Views from Chat WebSocket Example
# Credit to the Django Channels Chat WebSocket example
def chat(request):
    return render(request, 'cards/chat.html')


def room(request, room_name):
    return render(request, 'cards/room.html', {
        'room_name': room_name
    })


# Views for Login/Register/Logout from Previous Projects
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "cards/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "cards/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "cards/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "cards/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "cards/register.html")
