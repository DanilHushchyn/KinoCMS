# Generated by Django 5.0.6 on 2024-06-04 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0025_remove_movie_techs_movie_techs'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MovieTech',
        ),
    ]
