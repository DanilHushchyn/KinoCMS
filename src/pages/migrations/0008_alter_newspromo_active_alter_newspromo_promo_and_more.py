# Generated by Django 5.0.6 on 2024-06-12 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0007_remove_newspromo_cinema'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newspromo',
            name='active',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='newspromo',
            name='promo',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='newspromo',
            name='video_link',
            field=models.URLField(),
        ),
    ]
