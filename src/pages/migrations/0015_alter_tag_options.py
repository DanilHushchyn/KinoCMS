# -*- coding: utf-8 -*-
# Generated by Django 5.0.6 on 2024-07-06 11:53

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0014_alter_newspromo_tags"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="tag",
            options={
                "ordering": ["id"],
                "verbose_name": "Tag",
                "verbose_name_plural": "Tags",
            },
        ),
    ]
