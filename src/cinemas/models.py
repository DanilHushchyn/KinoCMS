from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from src.cinemas.managers.cinema import CinemaManager
from src.cinemas.managers.hall import HallManager
from src.core.models import Seo
from src.movies.models import TECHS_CHOICES
from src.movies.utils import MultiSelectField


# Create your models here.
class Cinema(Seo):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, db_index=True, null=True)
    description = models.TextField(max_length=20000)
    terms = models.JSONField()
    phone_1 = PhoneNumberField()
    phone_2 = PhoneNumberField()
    email = models.EmailField()
    banner = models.OneToOneField('core.Image',
                                  related_name='cin_bnr',
                                  on_delete=models.DO_NOTHING,
                                  null=True)
    logo = models.OneToOneField('core.Image',
                                on_delete=models.DO_NOTHING,
                                related_name='logo',
                                null=True)
    address = models.TextField(max_length=2000)
    coordinate = models.URLField(max_length=2000)
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
    description = models.TextField(max_length=20_000, null=True)
    banner = models.OneToOneField('core.Image', related_name='hall_bnr',
                                  on_delete=models.DO_NOTHING,
                                  null=True)
    layout = models.JSONField()
    date_created = models.DateTimeField(auto_now_add=True)
    cinema = models.ForeignKey('Cinema',
                               on_delete=models.CASCADE,
                               null=True)
    gallery = models.OneToOneField('core.Gallery',
                                   on_delete=models.DO_NOTHING,
                                   null=True)

    tech = models.CharField(choices=TECHS_CHOICES,
                            max_length=25)
    objects = HallManager()

    class Meta:
        ordering = ['-date_created']
        verbose_name = "Hall"
        unique_together = [['cinema', 'number'], ]
        verbose_name_plural = "Halls"
        db_table = 'halls'
