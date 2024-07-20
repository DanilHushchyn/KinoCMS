"""Module for testing pages"""

import pytest
from ninja_extra.testing import TestClient

import src.core.management.commands.init_script as init
import src.pages.endpoints.page as pg


@pytest.mark.django_db()
class TestCinemaAdminController:
    headers = {"Authorization": "Bearer admin"}
    client = TestClient(pg.PageController)

    @pytest.mark.parametrize(
        "pg_slug,expected_status",
        [
            (
                "stornka-05",
                200,
            ),
            (
                "stornka-00",
                404,
            ),
        ],
    )
    def test_get_page(self, pg_slug, expected_status):
        response = self.client.get(f"/{pg_slug}/", headers=self.headers)
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "payload, expected_status",
        [
            (
                {
                    "seo_title": "string",
                    "seo_description": "string",
                    "seo_image": {
                        "alt": "string",
                        "image": init.Command.create_image_b64("movie/card"),
                        "filename": "img.jpg",
                    },
                    "banner": {
                        "alt": "string",
                        "image": init.Command.create_image_b64("movie/card"),
                        "filename": "img.jpg",
                    },
                    "name_uk": "Сторінка",
                    "name_ru": "Страница",
                    "content_uk": "{}",
                    "content_ru": "{}",
                    "active": True,
                    "card_img": {
                        "alt": "string",
                        "image": init.Command.create_image_b64("movie/card"),
                        "filename": "img.jpg",
                    },
                },
                200,
            ),
            (
                {
                    "seo_title": "string",
                    "seo_description": "string",
                    "seo_image": {
                        "alt": "string",
                        "image": init.Command.create_image_b64("movie/card"),
                        "filename": "img.jpg",
                    },
                    "banner": {
                        "alt": "string",
                        "image": init.Command.create_image_b64("movie/card"),
                        "filename": "img.jpg",
                    },
                    "name_uk": "Сторінка - 01",
                    "name_ru": "Страница - 01",
                    "content_uk": "{}",
                    "content_ru": "{}",
                    "active": True,
                    "card_img": {
                        "alt": "string",
                        "image": init.Command.create_image_b64("movie/card"),
                        "filename": "img.jpg",
                    },
                },
                409,
            ),
        ],
    )
    def test_create_page(self, payload, expected_status):
        response = self.client.post("/", json=payload, headers=self.headers)
        assert response.status_code == expected_status

    def test_get_all_page_cards(self):
        response = self.client.get("/all-cards/", headers=self.headers)
        assert response.status_code == 200

    @pytest.mark.parametrize(
        "pg_slug, payload, expected_status",
        [
            (
                "stornka-03",
                {
                    "seo_title": "string",
                    "seo_description": "string",
                    "seo_image": {
                        "alt": "string",
                        "image": init.Command.create_image_b64("movie/card"),
                        "filename": "img.jpg",
                    },
                    "banner": {
                        "alt": "string",
                        "image": init.Command.create_image_b64("movie/card"),
                        "filename": "img.jpg",
                    },
                    "name_uk": "Сторінка",
                    "name_ru": "Страница",
                    "content_uk": "{}",
                    "content_ru": "{}",
                    "active": True,
                    "card_img": {
                        "alt": "string",
                        "image": init.Command.create_image_b64("movie/card"),
                        "filename": "img.jpg",
                    },
                },
                200,
            ),
            (
                "stornka-03",
                {},
                200,
            ),
            (
                "stornka-03",
                {
                    "seo_title": "string",
                    "seo_description": "string",
                    "seo_image": {
                        "alt": "string",
                        "image": init.Command.create_image_b64("movie/card"),
                        "filename": "img.jpg",
                    },
                    "banner": {
                        "alt": "string",
                        "image": init.Command.create_image_b64("movie/card"),
                        "filename": "img.jpg",
                    },
                    "name_uk": "Сторінка - 01",
                    "name_ru": "Страница - 01",
                    "active": True,
                    "card_img": {
                        "alt": "string",
                        "image": init.Command.create_image_b64("movie/card"),
                        "filename": "img.jpg",
                    },
                },
                409,
            ),
        ],
    )
    def test_update_page(self, pg_slug, payload, expected_status):
        response = self.client.patch(f"/{pg_slug}/", json=payload, headers=self.headers)
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "pg_slug,expected_status",
        [
            (
                "stornka-020",
                200,
            ),
            (
                "stornka-05",
                406,
            ),
            (
                "stornka-00",
                404,
            ),
        ],
    )
    def test_delete_page(self, pg_slug, expected_status):
        response = self.client.delete(f"/{pg_slug}/", headers=self.headers)
        assert response.status_code == expected_status
