from django.db import models

from src.core.models import Seo
from src.pages.managers.bottom_slider_item import BottomSliderItemManager
from src.pages.managers.news_promo import NewsPromoManager
from src.pages.managers.page import PageManager
from src.pages.managers.top_slider_item import TopSliderItemManager


# Create your models here.
class Page(Seo):
    name = models.CharField(max_length=60, unique=True, null=True)
    slug = models.SlugField(unique=True, null=True, db_index=True)
    content = models.JSONField()
    banner = models.OneToOneField('core.Image',
                                  on_delete=models.DO_NOTHING,
                                  null=True, related_name='page_bnr')
    active = models.BooleanField()
    can_delete = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    gallery = models.ForeignKey('core.Gallery',
                                on_delete=models.DO_NOTHING,
                                null=True)
    objects = PageManager()

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'
        db_table = 'pages'


class NewsPromo(Seo):
    name = models.CharField(max_length=60, unique=True, null=True)
    slug = models.SlugField(unique=True, null=True, db_index=True)
    description = models.TextField(null=True, max_length=20_000)
    banner = models.OneToOneField('core.Image',
                                  on_delete=models.DO_NOTHING,
                                  null=True, related_name='np_bnr')
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    active = models.BooleanField()
    promo = models.BooleanField()
    video_link = models.URLField()
    gallery = models.OneToOneField('core.Gallery',
                                   on_delete=models.DO_NOTHING,
                                   null=True)
    objects = NewsPromoManager()

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'News_Promo'
        verbose_name_plural = 'News_Promos'
        db_table = 'news_promos'


class BaseSlider(models.Model):
    active = models.BooleanField(null=True)
    TIMER_CHOICES = [
        [3, "3 сек"],
        [4, "4 сек"],
        [5, "5 сек"],
        [6, "6 сек"],
        [7, "7 сек"],
        [8, "8 сек"],
        [9, "9 сек"],
        [10, "10 сек"],
        [20, "20 сек"],
        [30, "30 сек"],
    ]
    speed = models.PositiveSmallIntegerField(null=True,
                                             choices=TIMER_CHOICES,
                                             default=30)

    class Meta:
        abstract = True
        verbose_name = 'BaseSlider'
        db_table = 'base_slider'


class TopSlider(BaseSlider):
    class Meta:
        verbose_name = 'TopSlider'
        verbose_name_plural = 'TopSliders'
        db_table = 'top_slider'


class BottomSlider(BaseSlider):
    class Meta:
        verbose_name = 'BottomSlider'
        verbose_name_plural = 'BottomSliders'
        db_table = 'bottom_slider'


class TopSliderItem(models.Model):
    url = models.URLField(null=True)
    text = models.CharField(max_length=40, null=True)
    image = models.OneToOneField('core.Image', related_name='top_sl_img',
                                 on_delete=models.DO_NOTHING,
                                 null=True)
    slider = models.ForeignKey(TopSlider, related_name='items',
                               on_delete=models.CASCADE,
                               null=True)
    objects = TopSliderItemManager()

    class Meta:
        verbose_name = 'TopSliderItem'
        verbose_name_plural = 'TopSliderItems'
        db_table = 'top_slider_item'


class BottomSliderItem(models.Model):
    url = models.URLField(null=True)
    image = models.OneToOneField('core.Image', related_name='bottom_sl_img',
                                 on_delete=models.DO_NOTHING,
                                 null=True)
    slider = models.ForeignKey(BottomSlider, related_name='items',
                               on_delete=models.CASCADE,
                               null=True)
    objects = BottomSliderItemManager()

    class Meta:
        verbose_name = 'BottomSliderItem'
        verbose_name_plural = 'BottomSliderItems'
        db_table = 'bottom_slider_item'


class ETEndBBanner(models.Model):
    image = models.OneToOneField('core.Image',
                                 on_delete=models.DO_NOTHING,
                                 null=True)
    color = models.CharField(null=True, max_length=40)
    use_img = models.BooleanField()

    class Meta:
        verbose_name = 'ETEndBBanner'
        verbose_name_plural = 'ETEndBBanners'
        db_table = 'etend_bbs'
