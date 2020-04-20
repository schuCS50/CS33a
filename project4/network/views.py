from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

import json
import time
from .models import User, Post


def index(request):
    return render(request, "network/index.html")


def following(request):
    return render(request, "network/following.html")


# API to assist in loading of posts with various request properties
def postHelper(request):
    # POST request process
    if request.method == "POST":
        data = json.loads(request.body)
        # If it has a post attribute, then it is an edit request
        if data.get("post") is not None:
            post = Post.objects.get(pk=data["post"])
            post.post = data["postText"]
        # If it does not, it is a net new post to save
        else:
            creator = User.objects.get(pk=request.user.id)
            post = Post(
                post=data['postText'],
                creator=creator
            )
        post.save()
        return JsonResponse({"message": "Post saved successfully."},
                            status=201)

    # We use the PUT request to handle likes
    elif request.method == "PUT":
        data = json.loads(request.body)
        # Must have relevant information to save like/unlike
        if data.get("post") is not None and data.get("liked") is not None:
            post = Post.objects.get(pk=data["post"])
            user = User.objects.get(pk=request.user.id)
            if data["liked"]:
                post.like.add(user)
            else:
                post.like.remove(user)
            return HttpResponse(status=204)
        else:
            return JsonResponse({"error": "Incorrect body elements."},
                                status=400)

    # If it is a GET request it will fit one of 4 cases...
    elif request.method == "GET":
        # If the page is requesting a single post, type will be 'single'
        if request.GET['type'] == 'single':
            if request.GET['postId'] != 'undefined':
                posts = Post.objects.filter(pk=request.GET['postId'])
            else:
                return JsonResponse({"error": "Must Have PostID."}, status=400)
        # If we need the users 'following' posts type will be 'following'
        elif request.GET['type'] == 'following':
            user = User.objects.get(pk=request.user.id).followedUser.all()
            posts = Post.objects.filter(creator__in=user).order_by(
                    "-createdTimestamp")
        # If we need a specific profile's  posts, type will be 'profile'
        elif request.GET['type'] == 'profile':
            if request.GET['username'] != 'undefined':
                user = User.objects.get(username=request.GET["username"])
                posts = Post.objects.filter(creator=user).order_by(
                    "-createdTimestamp")
            else:
                return JsonResponse({"error": "Must Have Username."},
                                    status=400)
        # Otherwise, we will return all posts
        else:
            posts = Post.objects.all().order_by("-createdTimestamp")

        # For the "like" option, we need to know who the user is
        try:
            requestUser = User.objects.get(pk=request.user.id)
            userid = requestUser.id
        except ObjectDoesNotExist:
            userid = -1
        print(userid)
        return JsonResponse([post.serialize(userid) for post in posts],
                            safe=False)

    else:
        return JsonResponse({"error": "Invalid Request Type."}, status=400)


def profile(request, username):
    profileUser = User.objects.filter(username=username).annotate(
                    Count('followedUser'))

    # We use the PUT request to update follow status
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("following") is not None:
            requestUser = User.objects.get(pk=request.user.id)
            if data["following"] == "True":
                requestUser.followedUser.remove(profileUser[0])
            else:
                requestUser.followedUser.add(profileUser[0])
            requestUser.save()
        return HttpResponse(status=204)

    # Logic to determine if the user follows this profile
    profileUser = User.objects.filter(username=username).annotate(
                    Count('followedUser'))
    followers = User.objects.filter(followedUser=profileUser[0].id)
    following = False
    for follower in followers:
        if follower.id == request.user.id:
            following = True

    # Render profile
    return render(request, "network/profile.html", {
        "profileUser": profileUser[0],
        "followers": len(followers),
        "following": following
    })


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
