# Generated by Django 5.1.5 on 2025-01-31 22:47

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("leagues", "0003_alter_league_users"),
    ]

    operations = [
        migrations.AddField(
            model_name="league",
            name="join_code",
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
