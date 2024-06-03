# Generated by Django 5.0.6 on 2024-06-03 15:10

import src.movies.utils
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0017_alter_movie_genres'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='genres',
            field=src.movies.utils.MultiSelectField(choices=[('comedy', 'Комедія'), ('fantasy', 'Фантастика'), ('horror', 'Жахи'), ('action', 'Бойовик'), ('melodramas', 'Мелодрами'), ('thriller', 'Трилер'), ('mysticism', 'Містика'), ('detective', 'Детектив')], max_length=40, null=True),
        ),
    ]
