from django.contrib import admin
from django.contrib.admin import ModelAdmin

from src.core.models import Image


# Register your models here.

# Register your models here.
@admin.register(Image)
class ImageAdmin(ModelAdmin):
    """
    Admin configuration for model Tag.

    """