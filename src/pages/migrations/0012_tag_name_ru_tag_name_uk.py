# Generated by Django 5.0.6 on 2024-07-06 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0011_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='name_ru',
            field=models.CharField(max_length=60, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='tag',
            name='name_uk',
            field=models.CharField(max_length=60, null=True, unique=True),
        ),
    ]
