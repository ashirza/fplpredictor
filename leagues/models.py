from django.contrib.auth.models import User
from django.db import models


class League(models.Model):
    name = models.CharField(max_length=64)
    users = models.ManyToManyField(User, related_name="leagues")
