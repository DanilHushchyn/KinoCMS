# Generated by Django 5.0.6 on 2024-05-20 17:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinemas', '0002_remove_cinema_seo_remove_hall_seo_and_more'),
        ('core', '0003_rename_galleryitem_galleryimage_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cinema',
            name='seo_image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_query_name='seo_img', to='core.image'),
        ),
        migrations.AlterField(
            model_name='hall',
            name='seo_image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_query_name='seo_img', to='core.image'),
        ),
    ]
