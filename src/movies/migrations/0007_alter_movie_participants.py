# -*- coding: utf-8 -*-
# Generated by Django 5.0.6 on 2024-07-06 20:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0006_alter_movie_participants"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="participants",
            field=models.ManyToManyField(to="movies.movieparticipant"),
        ),
    ]
