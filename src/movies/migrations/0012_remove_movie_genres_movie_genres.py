# Generated by Django 5.0.6 on 2024-06-03 08:39

import multiselectfield.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0011_movie_countries'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='genres',
        ),
        migrations.AddField(
            model_name='movie',
            name='genres',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Комедія'), (2, 'Фантастика'), (3, 'Жахи'), (4, 'Бойовик'), (5, 'Мелодрами'), (6, 'Трилер'), (7, 'Містика'), (8, 'Детектив')], default=1, max_length=40),
        ),
    ]
