# Generated by Django 5.0.6 on 2024-06-11 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinemas', '0011_alter_cinema_coordinate_alter_cinema_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cinema',
            name='coordinate',
            field=models.URLField(max_length=2000),
        ),
    ]
