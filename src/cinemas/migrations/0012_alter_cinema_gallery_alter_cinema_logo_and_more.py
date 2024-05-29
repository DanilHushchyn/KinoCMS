# Generated by Django 5.0.6 on 2024-05-29 13:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinemas', '0011_alter_cinema_banner'),
        ('core', '0004_alter_gallery_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cinema',
            name='gallery',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.gallery'),
        ),
        migrations.AlterField(
            model_name='cinema',
            name='logo',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, parent_link=True, related_name='logo', to='core.image'),
        ),
        migrations.AlterField(
            model_name='cinema',
            name='seo_image',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_query_name='seo_img', to='core.image'),
        ),
        migrations.AlterField(
            model_name='hall',
            name='banner',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, parent_link=True, related_name='hall_bnr', to='core.image'),
        ),
        migrations.AlterField(
            model_name='hall',
            name='schema',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, parent_link=True, related_name='schema', to='core.image'),
        ),
        migrations.AlterField(
            model_name='hall',
            name='seo_image',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_query_name='seo_img', to='core.image'),
        ),
    ]
