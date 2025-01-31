import uuid

from django.contrib.auth.models import User
from django.db import models


class League(models.Model):
    name = models.CharField(max_length=64)
    users = models.ManyToManyField(User, related_name="leagues")
    join_code = models.UUIDField(default=uuid.uuid4, editable=False)
