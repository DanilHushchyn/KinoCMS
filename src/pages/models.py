from django.db import models

from src.core.models import Seo


# Create your models here.
class Page(Seo):
    name = models.CharField(max_length=60, unique=True, null=True)
    slug = models.SlugField(unique=True, null=True, db_index=True)
    content = models.TextField(null=True)
    banner = models.OneToOneField('core.Image',
                                  on_delete=models.SET_NULL,
                                  null=True, related_name='page_bnr')
    active = models.BooleanField(null=True)
    can_delete = models.BooleanField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    # seo = models.OneToOneField('core.Seo', on_delete=models.CASCADE,
    #                            parent_link=True, null=True)
    gallery = models.ForeignKey('core.Gallery',
                                on_delete=models.SET_NULL,
                                null=True)

    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'
        db_table = 'pages'


class NewsPromo(Seo):
    name = models.CharField(max_length=60, unique=True, null=True)
    slug = models.SlugField(unique=True, null=True, db_index=True)
    content = models.TextField(null=True)
    banner = models.OneToOneField('core.Image',
                                  on_delete=models.SET_NULL,
                                  null=True, related_name='np_bnr')
    card_img = models.OneToOneField('core.Image',
                                    on_delete=models.SET_NULL,
                                    null=True, related_name='np_card')
    cinema = models.ForeignKey('cinemas.Cinema',
                               on_delete=models.CASCADE,
                               null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    active = models.BooleanField(null=True)
    promo = models.BooleanField(null=True)
    video_link = models.URLField(null=True)
    # seo = models.OneToOneField('core.Seo', on_delete=models.CASCADE,
    #                            parent_link=True, null=True)
    gallery = models.OneToOneField('core.Gallery',
                                   on_delete=models.SET_NULL,
                                   null=True)

    class Meta:
        verbose_name = 'News_Promo'
        verbose_name_plural = 'News_Promos'
        db_table = 'news_promos'


class Slider(models.Model):
    active = models.BooleanField(null=True)
    speed = models.PositiveSmallIntegerField(null=True)

    class Meta:
        verbose_name = 'Slider'
        verbose_name_plural = 'Sliders'
        db_table = 'sliders'


# class SliderItem(models.Model):
#     active = models.BooleanField(null=True)
#     speed = models.PositiveSmallIntegerField(null=True)
#
#     class Meta:
#         verbose_name = 'Slider'
#         verbose_name_plural = 'Sliders'
#         db_table = 'sliders'


class ETEndBBanner(models.Model):
    img = models.OneToOneField('core.Image',
                               on_delete=models.SET_NULL,
                               null=True)
    color = models.CharField(null=True, max_length=10)
    use_img = models.BooleanField(null=True)

    class Meta:
        verbose_name = 'ETEndBBanner'
        verbose_name_plural = 'ETEndBBanners'
        db_table = 'etend_bbs'
