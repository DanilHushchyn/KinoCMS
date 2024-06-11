# Generated by Django 5.0.6 on 2024-06-06 18:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_alter_movie_budget_alter_movie_duration_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='seo_description',
            field=models.CharField(max_length=160, validators=[django.core.validators.MinLengthValidator(50)]),
        ),
        migrations.AlterField(
            model_name='movie',
            name='seo_title',
            field=models.CharField(max_length=60),
        ),
    ]
