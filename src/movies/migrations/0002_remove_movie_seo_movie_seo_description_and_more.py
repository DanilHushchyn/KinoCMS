# Generated by Django 5.0.6 on 2024-05-20 17:05

import django.core.validators
import src.core.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='seo',
        ),
        migrations.AddField(
            model_name='movie',
            name='seo_description',
            field=models.CharField(max_length=160, null=True, validators=[django.core.validators.MinLengthValidator(50)]),
        ),
        migrations.AddField(
            model_name='movie',
            name='seo_image',
            field=models.ImageField(null=True, upload_to=src.core.utils.get_timestamp_path),
        ),
        migrations.AddField(
            model_name='movie',
            name='seo_title',
            field=models.CharField(max_length=60, null=True),
        ),
    ]
