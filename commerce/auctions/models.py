from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    
    def __str__(self):
        return f"{self.username}"

class Listing(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=64)
    description = models.TextField()
    startingBid = models.DecimalField(max_digits=11,decimal_places=2)
    image = models.URLField(blank=True)
    category = models.CharField(max_length=64, blank=True)
    active = models.BooleanField(default=True)
    createdTimestamp = models.DateTimeField(auto_now_add=True)
    updatedTimestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Listing {self.id}: {self.title} ({self.active})"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bid = models.DecimalField(max_digits=11,decimal_places=2)
    createdTimestamp = models.DateTimeField(auto_now_add=True)
    updatedTimestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Bid {self.id}: {self.user}-{self.listing} {self.bid}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    createdTimestamp = models.DateTimeField(auto_now_add=True)
    updatedTimestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment {self.id}: {self.user}-{self.listing}"

class WatchlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlistitems")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlists")
    active = models.BooleanField(null=True)
    createdTimestamp = models.DateTimeField(auto_now_add=True)
    updatedTimestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"WatchlistItem {self.id}: {self.user}-{self.listing}"