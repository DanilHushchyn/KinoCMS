# Generated by Django 5.0.6 on 2024-05-31 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinemas', '0017_alter_cinema_options_cinema_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='cinema',
            name='terms',
            field=models.JSONField(null=True),
        ),
    ]
