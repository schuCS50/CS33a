from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followedUser = models.ManyToManyField("self",
                                          symmetrical=False,
                                          blank=True,
                                          related_name="followers")

    def __str__(self):
        return f"User {self.id}: {self.username}"


class Post(models.Model):
    post = models.TextField()
    createdTimestamp = models.DateTimeField(auto_now_add=True)
    updatedTimestamp = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name="posts")
    like = models.ManyToManyField(User, blank=True, related_name="likes")

    def __str__(self):
        return f"Post {self.id}; Creator: {self.creator}; Text: {self.post}"

    # Function to return posts in a usable format with enriched properties
    def serialize(self, userid):
        return {
            "id": self.id,
            "creator": self.creator.username,
            "createdTimestamp": self.createdTimestamp.strftime(
                                "%b %d %Y, %I:%M %p"),
            "post": self.post,
            "likes": self.like.count(),
            "like": userid in [user.id for user in self.like.all()]
        }
