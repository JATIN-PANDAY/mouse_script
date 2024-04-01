# Generated by Django 5.0.3 on 2024-04-01 10:06

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "uid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("email", models.CharField(blank=True, max_length=100)),
                ("password", models.CharField(blank=True, max_length=100)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
