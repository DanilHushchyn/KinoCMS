from django.contrib import admin
from django.contrib.admin import ModelAdmin

from src.cinemas.models import Cinema


# Register your models here.
@admin.register(Cinema)
class CinemaAdmin(ModelAdmin):
    """
    Admin configuration for model Tag.

    """


