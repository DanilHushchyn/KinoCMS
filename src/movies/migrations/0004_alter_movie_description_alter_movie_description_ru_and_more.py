# Generated by Django 5.0.6 on 2024-06-11 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_alter_movie_seo_description_alter_movie_seo_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='description',
            field=models.TextField(max_length=20000),
        ),
        migrations.AlterField(
            model_name='movie',
            name='description_ru',
            field=models.TextField(max_length=20000, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='description_uk',
            field=models.TextField(max_length=20000, null=True),
        ),
    ]
