from django.db import models
from django.contrib.auth.models import User


class MatchingGameWord(models.Model):
    term = models.CharField(max_length=20)
    definition = models.CharField(max_length=100)

    def __str__(self):
        return self.term


class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scores')
    seconds = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} | {self.seconds}"
    

