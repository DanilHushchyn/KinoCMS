# Generated by Django 5.0.6 on 2024-06-06 18:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cinemas', '0003_alter_cinema_seo_description_alter_cinema_seo_title_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cinema',
            name='description_ru',
        ),
        migrations.RemoveField(
            model_name='cinema',
            name='description_uk',
        ),
        migrations.RemoveField(
            model_name='cinema',
            name='name_ru',
        ),
        migrations.RemoveField(
            model_name='cinema',
            name='name_uk',
        ),
        migrations.RemoveField(
            model_name='cinema',
            name='terms_ru',
        ),
        migrations.RemoveField(
            model_name='cinema',
            name='terms_uk',
        ),
    ]
