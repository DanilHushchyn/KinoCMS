import pytest
from ninja_extra.testing import TestClient

from ...core.management.commands.init_script import Command
from ..endpoints.hall import HallController


@pytest.mark.django_db()
class TestHallAdminController:
    headers = {"Authorization": "Bearer admin"}
    client = TestClient(HallController)

    @pytest.mark.parametrize(
        "hall_id,expected_status",
        [
            (
                1,
                200,
            ),
            (
                1111,
                404,
            ),
        ],
    )
    def test_get_hall(self, hall_id, expected_status):
        response = self.client.get(f"/{hall_id}/", headers=self.headers)
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
                        "image": Command.create_image_b64("hall/banner"),
                        "filename": "img.png",
                    },
                    "number": "1A",
                    "description_uk": "string",
                    "description_ru": "string",
                    "banner": {
                        "alt": "string",
                        "image": Command.create_image_b64("hall/banner"),
                        "filename": "img.jpg",
                    },
                    "gallery": [
                        {
                            "alt": "string",
                            "image": Command.create_image_b64("hall/banner"),
                            "filename": "img.jpg",
                        },
                        {
                            "alt": "string",
                            "image": Command.create_image_b64("hall/banner"),
                            "filename": "img.jpg",
                        },
                    ],
                },
                200,
            ),
            (
                {
                    "seo_title": "string",
                    "seo_description": "string",
                    "seo_image": {
                        "alt": "string",
                        "image": Command.create_image_b64("hall/banner"),
                        "filename": "img.png",
                    },
                    "number": "1A",
                    "description_uk": "string",
                    "description_ru": "string",
                    "banner": {
                        "alt": "string",
                        "image": Command.create_image_b64("hall/banner"),
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
                        "image": Command.create_image_b64("hall/banner"),
                        "filename": "img.png",
                    },
                    "number": "01",
                    "description_uk": "string",
                    "description_ru": "string",
                    "banner": {
                        "alt": "string",
                        "image": Command.create_image_b64("hall/banner"),
                        "filename": "img.jpg",
                    },
                },
                409,
            ),
        ],
    )
    def test_create_hall(self, payload, expected_status):
        response = self.client.post(
            "/?cnm_slug=knoteatr-01", json=payload, headers=self.headers
        )
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "hall_id, payload, expected_status",
        [
            (
                1,
                {
                    "seo_title": "string",
                    "seo_description": "string",
                    "seo_image": {
                        "alt": "string",
                        "image": Command.create_image_b64("cinema/banner"),
                        "filename": "img.jpg",
                    },
                    "number": "xxx",
                    "gallery": [
                        {
                            "alt": "string",
                            "image": Command.create_image_b64("cinema/banner"),
                            "filename": "img.jpg",
                            "delete": False,
                        },
                        {
                            "alt": "string",
                            "image": Command.create_image_b64("cinema/banner"),
                            "filename": "img.jpg",
                            "delete": False,
                        },
                    ],
                },
                200,
            ),
            (
                1,
                {
                    "number": "02",
                },
                409,
            ),
            (
                1,
                {},
                200,
            ),
        ],
    )
    def test_update_hall(self, hall_id, payload, expected_status):
        response = self.client.patch(f"/{hall_id}/", json=payload, headers=self.headers)
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "cnm_slug, expected_status",
        [
            (
                "knoteatr-01",
                200,
            ),
            (
                "knoteatr-01000",
                404,
            ),
        ],
    )
    def test_get_all_hall_cards(self, cnm_slug, expected_status):
        response = self.client.get(
            f"/all-cards/?cnm_slug={cnm_slug}", headers=self.headers
        )
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "hall_id, expected_status",
        [
            (
                1,
                200,
            ),
            (
                1111,
                404,
            ),
        ],
    )
    def test_delete_hall(self, hall_id, expected_status):
        response = self.client.delete(f"/{hall_id}/", headers=self.headers)
        assert response.status_code == expected_status
