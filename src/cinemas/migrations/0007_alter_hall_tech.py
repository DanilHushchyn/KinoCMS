# -*- coding: utf-8 -*-
# Generated by Django 5.0.6 on 2024-06-06 20:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cinemas", "0006_alter_hall_tech"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hall",
            name="tech",
            field=models.CharField(
                choices=[
                    ("3d", "3D"),
                    ("2d", "2D"),
                    ("imax", "IMAX"),
                    ("4dx.json", "4DX"),
                    ("5d", "5D"),
                ],
                max_length=25,
            ),
        ),
    ]
