from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, models
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, Bid, Comment, WatchlistItem

class BidForm(forms.Form):
    def __init__(self,listing_id, *args, **kwargs):
        super(BidForm, self).__init__(*args, **kwargs)
        self.listing_id = listing_id
        listing = Listing.objects.get(pk=listing_id)
        max_bid = Bid.objects.filter(listing=listing_id).aggregate(Max('bid'))
        if max_bid['bid__max']:
            self.min_bid = max_bid['bid__max']
        else:
            self.min_bid = listing.startingBid

    bid = forms.DecimalField(max_digits=11,decimal_places=2)

    def clean_bid(self):
        data = self.cleaned_data.get("bid")
        if self.min_bid >= data:
            message = "Bid too low, must bid at least " + str(self.min_bid)
            raise forms.ValidationError(message)
        return data

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(active=True).annotate(max_bid=Max('bids__bid'))
    })

def listing(request, listing_id):
    form = BidForm(listing_id)

    if request.method == "POST":
        form = BidForm(listing_id, request.POST)
        if form.is_valid():
            user = request.user
            listing = Listing.objects.get(pk=listing_id)
            new_bid = Bid.objects.create(user=user,listing=listing,bid=form.cleaned_data.get("bid"))
        
    return render(request, "auctions/listing.html", {
        "listing": Listing.objects.get(pk=listing_id),
        "bids": Bid.objects.filter(listing=listing_id),
        "comments": Comment.objects.filter(listing=listing_id),
        "form": form
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
