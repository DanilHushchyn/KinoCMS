# Generated by Django 5.0.6 on 2024-06-18 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_remove_seance_slug_remove_ticket_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seance',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
