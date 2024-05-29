# Generated by Django 5.0.6 on 2024-05-29 13:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinemas', '0012_alter_cinema_gallery_alter_cinema_logo_and_more'),
        ('core', '0004_alter_gallery_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cinema',
            name='banner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, parent_link=True, related_name='cin_bnr', to='core.image'),
        ),
        migrations.AlterField(
            model_name='cinema',
            name='gallery',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.gallery'),
        ),
        migrations.AlterField(
            model_name='cinema',
            name='logo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, parent_link=True, related_name='logo', to='core.image'),
        ),
        migrations.AlterField(
            model_name='hall',
            name='banner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, parent_link=True, related_name='hall_bnr', to='core.image'),
        ),
        migrations.AlterField(
            model_name='hall',
            name='gallery',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.gallery'),
        ),
        migrations.AlterField(
            model_name='hall',
            name='schema',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, parent_link=True, related_name='schema', to='core.image'),
        ),
    ]
