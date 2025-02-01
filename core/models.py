# core/models.py
from django.db import models
from django.contrib.auth.models import User


class Fixture(models.Model):
    external_id = models.IntegerField(unique=True)
    home_team = models.CharField(max_length=100)
    home_team_crest = models.URLField(max_length=500, null=True, blank=True)
    away_team = models.CharField(max_length=100)
    away_team_crest = models.URLField(max_length=500, null=True, blank=True)
    kickoff = models.DateTimeField()
    gameweek = models.IntegerField()
    status = models.CharField(max_length=20)
    home_score = models.IntegerField(null=True, blank=True)
    away_score = models.IntegerField(null=True, blank=True)


class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fixture = models.ForeignKey(Fixture, on_delete=models.CASCADE)
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    points = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "fixture"]
