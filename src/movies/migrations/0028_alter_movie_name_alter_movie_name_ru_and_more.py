# Generated by Django 5.0.6 on 2024-06-05 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0027_alter_movie_options_movie_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='name',
            field=models.CharField(max_length=60, unique=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='name_ru',
            field=models.CharField(max_length=60, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='name_uk',
            field=models.CharField(max_length=60, null=True, unique=True),
        ),
    ]
