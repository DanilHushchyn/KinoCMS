from django.core.validators import MinLengthValidator
from django.db import models

from src.core.utils import get_timestamp_path


# Create your models here.
class Seo(models.Model):
    # url = models.URLField()
    seo_title = models.CharField(max_length=60, null=True)
    seo_description = models.CharField(max_length=160,
                                       null=True,
                                       validators=
                                       [MinLengthValidator(50)])

    seo_image = models.ForeignKey('core.Image', on_delete=models.CASCADE,
                                  null=True, related_query_name='seo_img')

    class Meta:
        abstract = True
        verbose_name = 'Seo'
        db_table = 'seo'


class Image(models.Model):
    alt = models.CharField(max_length=60,
                           validators=[MinLengthValidator(1)])
    image = models.ImageField(upload_to=get_timestamp_path, null=True)

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
        db_table = 'images'


class Gallery(models.Model):
    class Meta:
        verbose_name = 'Gallery'
        verbose_name_plural = 'Galleries'
        db_table = 'gallery'


class GalleryImage(models.Model):
    image = models.ForeignKey('Image',
                              on_delete=models.CASCADE,
                              null=True, parent_link=True)

    gallery = models.ForeignKey('Gallery',
                                on_delete=models.CASCADE,
                                null=True)

    class Meta:
        verbose_name = 'GalleryImage'
        verbose_name_plural = 'GalleryImages'
        db_table = 'gallery_images'
