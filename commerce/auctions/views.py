from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, models
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Listing, Bid, Comment, WatchlistItem


class BidForm(forms.Form):
    def __init__(self, listing_id, *args, **kwargs):
        super(BidForm, self).__init__(*args, **kwargs)
        self.listing_id = listing_id
        listing = Listing.objects.get(pk=listing_id)
        max_bid = Bid.objects.filter(listing=listing_id).aggregate(Max('bid'))
        if max_bid['bid__max']:
            self.min_bid = max_bid['bid__max']
        else:
            self.min_bid = listing.startingBid

    bid = forms.DecimalField(max_digits=11, decimal_places=2)

    def clean_bid(self):
        data = self.cleaned_data.get("bid")
        if self.min_bid >= data:
            message = "Bid too low, must bid at least " + str(self.min_bid)
            raise forms.ValidationError(message)
        return data


class ListingForm(forms.Form):
    title = forms.CharField(max_length=64)
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control'}
    ))
    startingBid = forms.DecimalField(max_digits=11, decimal_places=2)
    image = forms.URLField(required=False)
    category = forms.CharField(required=False, max_length=64)

    title.widget.attrs.update({'class': 'form-control'})
    startingBid.widget.attrs.update({'class': 'form-control'})
    image.widget.attrs.update({'class': 'form-control'})
    category.widget.attrs.update({'class': 'form-control'})

    def clean_title(self):
        data = self.cleaned_data.get("title")
        try:
            Listing.objects.get(title=data)
        except ObjectDoesNotExist:
            return data
        else:
            message = "A listing with this title already exists"
            raise forms.ValidationError(message)


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(
            active=True).annotate(max_bid=Max('bids__bid'))
    })


def categories(request):
    result = Listing.objects.values('category').distinct()
    categories = []
    for category in result:
        categories.append(category['category'])

    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def category(request, category):
    return render(request, "auctions/category.html", {
        "category": category,
        "listings": Listing.objects.filter(
            active=True).filter(category=category).annotate(
                max_bid=Max('bids__bid'))
    })


def new(request):
    form = ListingForm()

    if request.method == "POST":
        form = ListingForm(request.POST)
        user = request.user
        if form.is_valid():
            Listing.objects.create(
                creator=user,
                title=form.cleaned_data.get("title"),
                description=form.cleaned_data.get("description"),
                startingBid=form.cleaned_data.get("startingBid"),
                image=form.cleaned_data.get("image"),
                category=form.cleaned_data.get("category"))
            return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/new.html", {
        "form": form
    })


def close(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        listing.active = False
        listing.save()

    return HttpResponseRedirect(reverse("index"))


def comment(request, listing_id):
    if request.method == "POST":
        user = request.user
        comment = request.POST['comment']
        listing = Listing.objects.get(pk=listing_id)
        print(comment)
        Comment.objects.create(user=user, listing=listing, comment=comment)

    return HttpResponseRedirect(reverse(
        "listing", kwargs={'listing_id': listing_id}))


def listing(request, listing_id):
    form = BidForm(listing_id)
    user = request.user
    listing = Listing.objects.get(pk=listing_id)

    if request.method == "POST":
        form = BidForm(listing_id, request.POST)
        if form.is_valid():
            Bid.objects.create(
                user=user, listing=listing, bid=form.cleaned_data.get("bid"))

    max_bid = Bid.objects.filter(listing=listing).order_by("-bid")[:1]

    if len(max_bid) == 0:
        max_bid = None
    else:
        max_bid = max_bid[0]

    if user.is_authenticated:
        try:
            item = WatchlistItem.objects.get(user=user, listing=listing)
        except ObjectDoesNotExist:
            watching = False
        else:
            if item.active:
                watching = True
            else:
                watching = False
    else:
        watching = False

    return render(request, "auctions/listing.html", {
        "listing": Listing.objects.get(pk=listing_id),
        "bids": Bid.objects.filter(listing=listing_id).order_by("-bid"),
        "comments": Comment.objects.filter(
            listing=listing_id).order_by("-createdTimestamp"),
        "form": form,
        "watching": watching,
        "max_bid": max_bid
    })


def watchlist(request):
    user = request.user

    if request.method == "POST":
        listing_id = request.POST['listingid']
        action = request.POST['action']
        listing = Listing.objects.get(pk=listing_id)
        try:
            item = WatchlistItem.objects.get(user=user, listing=listing)
            if action == 'ADD':
                item.active = True
            else:
                item.active = False
            item.save()
        except ObjectDoesNotExist:
            WatchlistItem.objects.create(user=user, listing=listing)
    items = Listing.objects.filter(watchlists__user=user).filter(
        watchlists__active=True).annotate(max_bid=Max('bids__bid'))
    return render(request, "auctions/watchlist.html", {
        "listings": items
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
