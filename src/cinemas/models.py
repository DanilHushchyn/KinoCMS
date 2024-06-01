from django.db import models

from src.cinemas.managers.cinema import CinemaManager
from src.core.models import Seo


# Create your models here.
class Cinema(Seo):
    name = models.CharField(max_length=100, unique=True, null=True)
    slug = models.SlugField(unique=True, db_index=True, null=True)
    description = models.TextField(max_length=2000, null=True)
    terms = models.JSONField(null=True)
    banner = models.OneToOneField('core.Image',
                                  related_name='cin_bnr',
                                  on_delete=models.DO_NOTHING,
                                  null=True)
    logo = models.OneToOneField('core.Image',
                                on_delete=models.DO_NOTHING,
                                related_name='logo',
                                null=True)
    address = models.TextField(max_length=2000, null=True)
    coordinate = models.CharField(max_length=2000, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    gallery = models.OneToOneField('core.Gallery',
                                   on_delete=models.DO_NOTHING,
                                   null=True)
    objects = CinemaManager()

    class Meta:
        ordering = ['-date_created', ]
        verbose_name = "Cinema"
        verbose_name_plural = "Cinemas"
        db_table = 'cinemas'


class Hall(Seo):
    number = models.CharField(max_length=60)
    slug = models.SlugField(db_index=True, unique=True, null=True)
    description = models.TextField(max_length=2000, null=True)
    banner = models.OneToOneField('core.Image', related_name='hall_bnr',
                                  on_delete=models.DO_NOTHING,
                                  null=True)
    schema = models.OneToOneField('core.Image', related_name='schema',
                                  on_delete=models.DO_NOTHING,
                                  null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    cinema = models.ForeignKey('Cinema',
                               on_delete=models.CASCADE,
                               null=True)
    gallery = models.OneToOneField('core.Gallery',
                                   on_delete=models.DO_NOTHING,
                                   null=True)

    class Meta:
        verbose_name = "Hall"
        unique_together = [['cinema', 'number'], ]
        verbose_name_plural = "Halls"
        db_table = 'halls'
