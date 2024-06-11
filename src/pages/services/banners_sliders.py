from typing import Type, List

from django.db.models import Model, Q
from injector import inject
from ninja.errors import HttpError
from django.utils.translation import gettext as _

from src.core.schemas.base import MessageOutSchema
from src.core.services.images import ImageService
from src.core.utils import primitives
from src.pages.models import (TopSlider, TopSliderItem, BaseSlider,
                              BottomSlider, BottomSliderItem,
                              ETEndBBanner)
from src.pages.schemas.banners_sliders import (TopSliderUpdateSchema,
                                               TopSliderItemUpdateSchema,
                                               BottomSliderUpdateSchema,
                                               BottomSliderItemUpdateSchema,
                                               ETEndBBannerUpdateSchema)

from django.db import transaction


class SliderService:
    """
    A service class for solving common task in our system.
    """

    @inject
    def __init__(self, image_service: ImageService):
        self.image_service = image_service

    @staticmethod
    def get_speed_choices() -> List:
        """
        Get all speed choices for slider.
        """

        speed_choices = BaseSlider.TIMER_CHOICES
        return speed_choices

    def update_top_slider(self, schema: TopSliderUpdateSchema) \
            -> MessageOutSchema:
        """
        Update Top Slider.
        """

        top_slider = self.get_top_slider()
        self.update_slider_items(schemas=schema.items,
                                 slider=top_slider)
        for key, value in schema.dict().items():
            if isinstance(value, primitives):
                setattr(top_slider, key, value)
        top_slider.save()
        msg = _('Верхній слайдер успішно оновлений')
        return MessageOutSchema(detail=msg)

    def update_bottom_slider(self, schema: BottomSliderUpdateSchema) \
            -> MessageOutSchema:
        """
        Update Bottom Slider.
        """

        bottom_slider = self.get_bottom_slider()
        self.update_slider_items(schemas=schema.items,
                                 slider=bottom_slider)
        for key, value in schema.dict().items():
            if isinstance(value, primitives):
                setattr(bottom_slider, key, value)
        bottom_slider.save()
        msg = _('Нижній слайдер успішно оновлений')
        return MessageOutSchema(detail=msg)

    @staticmethod
    def get_top_slider() \
            -> TopSlider:
        """
        Get Top Slider.
        """
        try:
            top_slider = (TopSlider.objects
                          .prefetch_related('items__image')
                          .get(id=1))
        except TopSlider.DoesNotExist:
            msg = "TopSlider doesn't exist.Backend have to add"
            raise HttpError(404, msg)
        return top_slider

    @staticmethod
    def get_bottom_slider() \
            -> BottomSlider:
        """
        Get Bottom Slider.
        """
        try:
            bottom_slider = (BottomSlider.objects
                             .prefetch_related('items__image')
                             .get(id=1))
        except BottomSlider.DoesNotExist:
            msg = "BottomSlider doesn't exist.Backend have to add"
            raise HttpError(404, msg)
        return bottom_slider

    def update_slider_items(self,
                            schemas: List[TopSliderItemUpdateSchema] |
                                     List[BottomSliderItemUpdateSchema],
                            slider: TopSlider | BottomSlider) -> None:
        """
        Update Slider.
        """
        del_item_ids = []
        item_ids = []
        update_items_dict = {}
        create_item_schemas = []
        if schemas:
            for schema in schemas:
                if schema.id:
                    item_ids.append(schema.id)
                    if schema.delete:
                        del_item_ids.append(schema.id)
                    else:
                        update_items_dict[schema.id] = schema
                elif not schema.delete:
                    for key, value in schema.dict().items():
                        if value is None and key != 'id':
                            msg = ("You provided no correct "
                                   "data for creating new slider item. "
                                   "Each field is required(except id) "
                                   "if you are creating an element.")
                            raise HttpError(403, msg)
                    create_item_schemas.append(schema)
            db_ids = slider.items.model.objects.values_list('id', flat=True)
            for item_id in item_ids:
                if item_id not in db_ids:
                    msg = (f"Given "
                           f"{slider.items.model.__name__} "
                           f"with id {item_id} "
                           f"doesn't belongs to "
                           f"{slider._meta.model.__name__}")
                    raise HttpError(404, msg)
            self.bulk_delete_slider_items(item_ids=del_item_ids,
                                          slider=slider)
            self.bulk_update_slider_items(items_dict=update_items_dict,
                                          slider=slider)
            sliders_length = (slider.items.count() +
                              len(create_item_schemas))
            if sliders_length >= 10:
                msg = _('Максимальна кількість елементів '
                        'верхнього банеру, 10')
                raise HttpError(409, msg)
            self.bulk_create_slider_items(item_schemas=create_item_schemas,
                                          slider=slider)

    def bulk_create_slider_items(self,
                                 item_schemas:
                                 List[TopSliderItemUpdateSchema] |
                                 List[BottomSliderItemUpdateSchema],
                                 slider: TopSlider | BottomSlider) \
            -> None:
        """
        Create multiple slider's items by list of schemas.
        """
        if item_schemas:
            image_schemas = []
            new_items = []
            for schema in item_schemas:
                image_schemas.append(schema.image)
                init_data = schema
                init_data.image = None
                del init_data.delete
                new_items.append(slider.items.model(
                    **init_data.dict(),
                    slider=slider
                ))
            imgs_list = self.image_service.bulk_create(image_schemas)
            for img, item in zip(imgs_list, new_items):
                item.image = img
            slider.items.model.objects.bulk_create(new_items)

    def bulk_update_slider_items(self, items_dict: dict,
                                 slider: TopSlider | BottomSlider) \
            -> None:
        """
        Update multiple slider's items by list of ids.
        """
        if items_dict:
            slider_items = (slider.items.model.objects
                            .filter(id__in=items_dict.keys()))
            fields = []
            for (key, schema), item in zip(items_dict.items(), slider_items):
                for attr, value in schema.dict().items():
                    if isinstance(value, primitives):
                        setattr(item, attr, value)
                        if attr not in fields:
                            fields.append(attr)
                if schema.image:
                    with transaction.atomic():
                        self.image_service.update(schema.image,
                                                  item.image)
            fields.remove('id')
            fields.remove('delete')
            slider.items.model.objects.bulk_update(slider_items, fields)

    # def update_bottom_slider_items(self,
    #                                schemas:
    #                                List[BottomSliderItemUpdateSchema],
    #                                slider: BottomSlider) -> None:
    #     """
    #     Update Bottom Slider.
    #     """
    #     if schemas:
    #         for schema in schemas:
    #             if schema.id:
    #                 slider_item = (BottomSliderItem.objects
    #                                .get_by_id(schema.id))
    #                 self.item_matches_slider(slider, schema.id)
    #                 if schema.delete:
    #                     slider_item.delete()
    #                     self.image_service.delete(slider_item.image)
    #                 else:
    #                     self.image_service.update(schema.image,
    #                                               slider_item.image)
    #                     expt_list = ['image', ]
    #                     for attr, value in schema.dict().items():
    #                         if attr not in expt_list and value is not None:
    #                             setattr(slider_item, attr, value)
    #                     slider_item.save()
    #             elif not schema.delete:
    #                 for key, value in schema.dict().items():
    #                     if value is None and key != 'id':
    #                         msg = ("You provided no correct "
    #                                "data for creating new slider item. "
    #                                "Each field is required(except id) "
    #                                "if you are creating element.")
    #                         raise HttpError(403, msg)
    #                 if slider.items.count() >= 10:
    #                     msg = _('Максимальна кількість елементів '
    #                             'верхнього банеру, 10')
    #                     raise HttpError(409, msg)
    #                 image = self.image_service.create(schema.image)
    #                 item = BottomSliderItem.objects.create(
    #                     url=schema.url,
    #                     image=image,
    #                 )
    #                 slider.items.add(item)
    #                 slider.save()

    def bulk_delete_slider_items(self, item_ids: List[int],
                                 slider: TopSlider | BottomSlider) \
            -> None:
        """
        Delete multiple slider's items by list of ids.
        """
        items = slider.items.filter(id__in=item_ids)
        img_ids = list(items.values_list('image_id', flat=True))
        items.delete()
        self.image_service.bulk_delete(img_ids)

    # @staticmethod
    # def item_matches_slider(slider: TopSlider | BottomSlider,
    #                         item_id: int) -> None:
    #     """
    #     Check that item match to given slider.
    #     """
    #     ids = slider.items.values_list('id', flat=True)
    #     if item_id not in ids:
    #         msg = "Given item_ id doesn't belongs to slider"
    #         raise HttpError(404, msg)

    @staticmethod
    def get_etend_banner() \
            -> ETEndBBanner:
        """
        Get ETEndBBanner.
        """
        try:
            etend_banner = ETEndBBanner.objects.get(id=1)
        except ETEndBBanner.DoesNotExist:
            msg = "ETEndBanner doesn't exist. Backend have to add"
            raise HttpError(404, msg)

        return etend_banner

    def update_etend_banner(self, schema: ETEndBBannerUpdateSchema) \
            -> MessageOutSchema:
        """
        Update ETEndBBanner.
        """

        etend_banner = self.get_etend_banner()
        self.image_service.update(schema.image,
                                  etend_banner.image)
        for key, value in schema.dict().items():
            if isinstance(value, primitives):
                setattr(etend_banner, key, value)
        etend_banner.save()
        msg = _('Наскрізний банер успішно оновлений')
        return MessageOutSchema(detail=msg)
