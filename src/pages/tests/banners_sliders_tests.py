"""Module for testing banners and sliders"""

import random

import pytest
from ninja_extra.testing import TestClient

import src.core.management.commands.init_script as init
import src.pages.endpoints.banners_sliders as bs
from src.pages.models import BottomSliderItem
from src.pages.models import TopSliderItem


@pytest.mark.django_db()
class TestBannersSlidersController:
    headers = {"Authorization": "Bearer admin"}
    client = TestClient(bs.SliderController)

    def test_get_top_slider(self):
        response = self.client.get("/top/", headers=self.headers)
        assert response.status_code == 200

    def test_get_bottom_slider(self):
        response = self.client.get("/bottom/", headers=self.headers)
        assert response.status_code == 200

    def test_get_etend_banner(self):
        response = self.client.get("/etend-banner/", headers=self.headers)
        assert response.status_code == 200

    def test_create_top_slider_item(self):
        before = TopSliderItem.objects.count()
        # test create
        response = self.client.patch(
            "/top/",
            json={
                "items": [
                    {
                        "image": {
                            "alt": "string",
                            "image": init.Command.create_image_b64("top_slider"),
                            "filename": "string.jpg",
                        },
                        "url": "https://www.youtube.com/",
                        "text_uk": "string",
                        "text_ru": "string",
                        "delete": False,
                    },
                    {
                        "image": {
                            "alt": "string",
                            "image": init.Command.create_image_b64("top_slider"),
                            "filename": "string.jpg",
                        },
                        "url": "https://www.youtube.com/",
                        "text_uk": "string",
                        "text_ru": "string",
                        "delete": False,
                    },
                ]
            },
            headers=self.headers,
        )
        assert response.status_code == 200
        assert TopSliderItem.objects.count() == before + 2

    def test_update_top_slider_item(self):
        item_ids = list(TopSliderItem.objects.values_list("id", flat=True))
        # test create
        response = self.client.patch(
            "/top/",
            json={
                "items": [
                    {
                        "id": random.choice(item_ids),
                        "image": {
                            "alt": "string",
                            "image": init.Command.create_image_b64("top_slider"),
                            "filename": "string.jpg",
                        },
                        "url": "https://www.youtube.com/",
                        "text_uk": "new text",
                        "text_ru": "new text",
                        "delete": False,
                    }
                ]
            },
            headers=self.headers,
        )
        assert response.status_code == 200

    def test_delete_top_slider_item(self):
        item_ids = list(TopSliderItem.objects.values_list("id", flat=True))
        before = TopSliderItem.objects.count()
        response = self.client.patch(
            "/top/",
            json={
                "items": [
                    {"id": random.choice(item_ids), "delete": True},
                ]
            },
            headers=self.headers,
        )

        assert response.status_code == 200
        after = TopSliderItem.objects.count()
        assert after == before - 1

    def test_create_bottom_slider_item(self):
        before = BottomSliderItem.objects.count()
        # test create
        response = self.client.patch(
            "/bottom/",
            json={
                "items": [
                    {
                        "image": {
                            "alt": "string",
                            "image": init.Command.create_image_b64("top_slider"),
                            "filename": "string.jpg",
                        },
                        "url": "https://www.youtube.com/",
                        "delete": False,
                    },
                    {
                        "image": {
                            "alt": "string",
                            "image": init.Command.create_image_b64("top_slider"),
                            "filename": "string.jpg",
                        },
                        "url": "https://www.youtube.com/",
                        "delete": False,
                    },
                ]
            },
            headers=self.headers,
        )
        assert response.status_code == 200
        assert BottomSliderItem.objects.count() == before + 2

    def test_update_bottom_slider_item(self):
        item_ids = list(BottomSliderItem.objects.values_list("id", flat=True))
        # test create
        response = self.client.patch(
            "/bottom/",
            json={
                "items": [
                    {
                        "id": random.choice(item_ids),
                        "image": {
                            "alt": "string",
                            "image": init.Command.create_image_b64("top_slider"),
                            "filename": "string.jpg",
                        },
                        "url": "https://www.youtube.com/",
                        "delete": False,
                    }
                ]
            },
            headers=self.headers,
        )
        assert response.status_code == 200

    def test_delete_bottom_slider_item(self):
        item_ids = list(BottomSliderItem.objects.values_list("id", flat=True))
        before = BottomSliderItem.objects.count()
        response = self.client.patch(
            "/bottom/",
            json={
                "items": [
                    {"id": random.choice(item_ids), "delete": True},
                ]
            },
            headers=self.headers,
        )

        assert response.status_code == 200
        after = BottomSliderItem.objects.count()
        assert after == before - 1

    @pytest.mark.parametrize(
        "payload, expected_status",
        [
            (
                {
                    "image": {
                        "alt": "string",
                        "image": init.Command.create_image_b64("top_slider"),
                        "filename": "string.jpg",
                    },
                    "color": "#8ad4f0",
                    "use_img": True,
                },
                200,
            ),
            (
                {
                    "image": {
                        "alt": "string",
                        "image": init.Command.create_image_b64("top_slider"),
                        "filename": "string.jpg",
                    },
                    "color": "string",
                    "use_img": True,
                },
                422,
            ),
        ],
    )
    def test_update_etend_banner(self, payload, expected_status):
        response = self.client.patch(
            "/etend-banner/", json=payload, headers=self.headers
        )
        assert response.status_code == expected_status
