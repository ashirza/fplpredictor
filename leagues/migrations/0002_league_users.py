# Generated by Django 5.1.5 on 2025-01-31 19:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("leagues", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="league",
            name="users",
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
