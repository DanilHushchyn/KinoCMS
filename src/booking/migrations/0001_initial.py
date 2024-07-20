# -*- coding: utf-8 -*-
# Generated by Django 5.0.6 on 2024-06-06 18:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("cinemas", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Seance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("slug", models.SlugField(null=True, unique=True)),
                ("tech_type", models.CharField(max_length=60)),
                ("price", models.PositiveIntegerField(null=True)),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "hall",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cinemas.cinema",
                    ),
                ),
            ],
            options={
                "verbose_name": "Seance",
                "verbose_name_plural": "Seances",
                "db_table": "seances",
            },
        ),
        migrations.CreateModel(
            name="Ticket",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("row", models.PositiveIntegerField(null=True)),
                ("seat", models.PositiveIntegerField(null=True)),
                (
                    "seance",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="booking.seance",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Ticket",
                "verbose_name_plural": "Tickets",
                "db_table": "tickets",
            },
        ),
    ]
