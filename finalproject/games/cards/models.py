from django.contrib.auth.models import AbstractUser
from django.db import models

# Extended user class
class User(AbstractUser):
    def __str__(self):
        return f"User {self.id}: {self.username}"

# Two Player Game extendable 
class TwoPlayerGame(models.Model):
    player1 = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name="p1_games")
    player2 = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name="p2_games")
    createdTimestamp = models.DateTimeField(auto_now_add=True)
    updatedTimestamp = models.DateTimeField(auto_now=True)
    winner = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="won_games",
                               blank=True,
                               null=True)

    class Meta:
        abstract = True

#TicTacToe Game
class TicTacToe(TwoPlayerGame):
    cell1 = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name="cell1",
                              blank=True,
                              null=True)
    cell2 = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name="cell2",
                              blank=True,
                              null=True)
    cell3 = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name="cell3",
                              blank=True,
                              null=True)
    cell4 = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name="cell4",
                              blank=True,
                              null=True)
    cell5 = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name="cell5",
                              blank=True,
                              null=True)
    cell6 = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name="cell6",
                              blank=True,
                              null=True)
    cell7 = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name="cell7",
                              blank=True,
                              null=True)
    cell8 = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name="cell8",
                              blank=True,
                              null=True)
    cell9 = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name="cell9",
                              blank=True,
                              null=True)

    # Function to return formatted output
    def serialize(self):
        return {
            "player1": self.player1.username,
            "player2": self.player2.username,
            "createdTimestamp": self.createdTimestamp.strftime(
                                "%b %d %Y, %I:%M %p"),
            "updatedTimestamp": self.updatedTimestamp.strftime(
                                "%b %d %Y, %I:%M %p"),
            "winner": self.winner.username if self.winner else None,
            "cells": [self.cell1.username if self.cell1 else None,
                      self.cell2.username if self.cell2 else None,
                      self.cell3.username if self.cell3 else None,
                      self.cell4.username if self.cell4 else None,
                      self.cell5.username if self.cell5 else None,
                      self.cell6.username if self.cell6 else None,
                      self.cell7.username if self.cell7 else None,
                      self.cell8.username if self.cell8 else None,
                      self.cell9.username if self.cell9 else None]
        }