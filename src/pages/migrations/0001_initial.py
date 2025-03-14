# -*- coding: utf-8 -*-
# Generated by Django 5.0.6 on 2024-06-06 18:26

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("cinemas", "0001_initial"),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="BottomSlider",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("active", models.BooleanField(null=True)),
                (
                    "speed",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (3, "3S"),
                            (4, "4S"),
                            (5, "5S"),
                            (6, "6S"),
                            (7, "7S"),
                            (8, "8S"),
                            (9, "9S"),
                            (10, "10S"),
                            (20, "20S"),
                            (30, "30S"),
                        ],
                        default=30,
                        null=True,
                    ),
                ),
            ],
            options={
                "verbose_name": "BottomSlider",
                "verbose_name_plural": "BottomSliders",
                "db_table": "bottom_slider",
            },
        ),
        migrations.CreateModel(
            name="TopSlider",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("active", models.BooleanField(null=True)),
                (
                    "speed",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (3, "3S"),
                            (4, "4S"),
                            (5, "5S"),
                            (6, "6S"),
                            (7, "7S"),
                            (8, "8S"),
                            (9, "9S"),
                            (10, "10S"),
                            (20, "20S"),
                            (30, "30S"),
                        ],
                        default=30,
                        null=True,
                    ),
                ),
            ],
            options={
                "verbose_name": "TopSlider",
                "verbose_name_plural": "TopSliders",
                "db_table": "top_slider",
            },
        ),
        migrations.CreateModel(
            name="BottomSliderItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("url", models.URLField(null=True)),
                (
                    "image",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="bottom_sl_img",
                        to="core.image",
                    ),
                ),
                (
                    "slider",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="pages.bottomslider",
                    ),
                ),
            ],
            options={
                "verbose_name": "BottomSliderItem",
                "verbose_name_plural": "BottomSliderItems",
                "db_table": "bottom_slider_item",
            },
        ),
        migrations.CreateModel(
            name="ETEndBBanner",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("color", models.CharField(max_length=10, null=True)),
                ("use_img", models.BooleanField(null=True)),
                (
                    "img",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="core.image",
                    ),
                ),
            ],
            options={
                "verbose_name": "ETEndBBanner",
                "verbose_name_plural": "ETEndBBanners",
                "db_table": "etend_bbs",
            },
        ),
        migrations.CreateModel(
            name="NewsPromo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("seo_title", models.CharField(max_length=60, null=True)),
                (
                    "seo_description",
                    models.CharField(
                        max_length=160,
                        null=True,
                        validators=[django.core.validators.MinLengthValidator(50)],
                    ),
                ),
                ("name", models.CharField(max_length=60, null=True, unique=True)),
                ("slug", models.SlugField(null=True, unique=True)),
                ("content", models.TextField(null=True)),
                ("date_created", models.DateTimeField(auto_now_add=True, null=True)),
                ("active", models.BooleanField(null=True)),
                ("promo", models.BooleanField(null=True)),
                ("video_link", models.URLField(null=True)),
                (
                    "banner",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="np_bnr",
                        to="core.image",
                    ),
                ),
                (
                    "card_img",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="np_card",
                        to="core.image",
                    ),
                ),
                (
                    "cinema",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cinemas.cinema",
                    ),
                ),
                (
                    "gallery",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="core.gallery",
                    ),
                ),
                (
                    "seo_image",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_query_name="seo_img",
                        to="core.image",
                    ),
                ),
            ],
            options={
                "verbose_name": "News_Promo",
                "verbose_name_plural": "News_Promos",
                "db_table": "news_promos",
            },
        ),
        migrations.CreateModel(
            name="Page",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("seo_title", models.CharField(max_length=60, null=True)),
                (
                    "seo_description",
                    models.CharField(
                        max_length=160,
                        null=True,
                        validators=[django.core.validators.MinLengthValidator(50)],
                    ),
                ),
                ("name", models.CharField(max_length=60, null=True, unique=True)),
                ("slug", models.SlugField(null=True, unique=True)),
                ("content", models.TextField(null=True)),
                ("active", models.BooleanField(null=True)),
                ("can_delete", models.BooleanField(null=True)),
                ("date_created", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "banner",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="page_bnr",
                        to="core.image",
                    ),
                ),
                (
                    "gallery",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="core.gallery",
                    ),
                ),
                (
                    "seo_image",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_query_name="seo_img",
                        to="core.image",
                    ),
                ),
            ],
            options={
                "verbose_name": "Page",
                "verbose_name_plural": "Pages",
                "db_table": "pages",
            },
        ),
        migrations.CreateModel(
            name="TopSliderItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("url", models.URLField(null=True)),
                ("text", models.CharField(max_length=40, null=True)),
                ("text_uk", models.CharField(max_length=40, null=True)),
                ("text_ru", models.CharField(max_length=40, null=True)),
                (
                    "image",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="top_sl_img",
                        to="core.image",
                    ),
                ),
                (
                    "slider",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="pages.topslider",
                    ),
                ),
            ],
            options={
                "verbose_name": "TopSliderItem",
                "verbose_name_plural": "TopSliderItems",
                "db_table": "top_slider_item",
            },
        ),
    ]
