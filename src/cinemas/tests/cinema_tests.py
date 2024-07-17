import pytest
from ninja_extra.testing import TestClient
from ..endpoints.cinema import CinemaController
from ...core.management.commands.init_script import Command


@pytest.mark.django_db
class TestCinemaAdminController:
    headers = {
        'Authorization': 'Bearer admin'
    }
    client = TestClient(CinemaController)

    @pytest.mark.parametrize("cnm_slug,expected_status",
                             [
                                 (

                                         "knoteatr-01",
                                         200,
                                 ),
                                 (

                                         "knoteatr-00",
                                         404,
                                 ),
                             ]
                             )
    def test_get_cinema(self, cnm_slug, expected_status):
        response = self.client.get(f"/{cnm_slug}/",
                                   headers=self.headers)
        assert response.status_code == expected_status

    @pytest.mark.parametrize("payload, expected_status",
                             [
                                 (

                                         {
                                             "seo_title": "string",
                                             "seo_description": "string",
                                             "seo_image": {
                                                 "alt": "string",
                                                 "image": Command.create_image_b64('cinema/banner'),
                                                 "filename": 'img.png',
                                             },
                                             "name_uk": "Кінотеатр",
                                             "name_ru": "Кинотеатр",
                                             "description_uk": "string",
                                             "description_ru": "string",
                                             "terms_uk": "{}",
                                             "terms_ru": "{}",
                                             "phone_1": "+380985412554",
                                             "phone_2": "+380985412554",
                                             "email": "user@example.com",
                                             "banner": {
                                                 "alt": "string",
                                                 "image": Command.create_image_b64('cinema/banner'),
                                                 "filename": 'img.jpg',
                                             },
                                             "logo": {
                                                 "alt": "string",
                                                 "image": Command.create_image_b64('cinema/logo'),
                                                 "filename": 'img.svg',
                                             },
                                             "address_uk": "string",
                                             "address_ru": "string",
                                             "coordinate": "https://example.com/",
                                             "gallery": [
                                                 {
                                                     "alt": "string",
                                                     "image": Command.create_image_b64('cinema/banner'),
                                                     "filename": 'img.jpg',
                                                 },
                                                 {
                                                     "alt": "string",
                                                     "image": Command.create_image_b64('cinema/banner'),
                                                     "filename": 'img.jpg',
                                                 }
                                             ]
                                         },
                                         200,
                                 ),
                                 (

                                         {
                                             "seo_title": "string",
                                             "seo_description": "string",
                                             "seo_image": {
                                                 "alt": "string",
                                                 "image": Command.create_image_b64('cinema/banner'),
                                                 "filename": 'img.png',
                                             },
                                             "name_uk": "Кінотеатр",
                                             "name_ru": "Кинотеатр",
                                             "description_uk": "string",
                                             "description_ru": "string",
                                             "terms_uk": "{}",
                                             "terms_ru": "{}",
                                             "phone_1": "+380985412554",
                                             "phone_2": "+380985412554",
                                             "email": "user@example.com",
                                             "banner": {
                                                 "alt": "string",
                                                 "image": Command.create_image_b64('cinema/banner'),
                                                 "filename": 'img.jpg',
                                             },
                                             "logo": {
                                                 "alt": "string",
                                                 "image": Command.create_image_b64('cinema/logo'),
                                                 "filename": 'img.svg',
                                             },
                                             "address_uk": "string",
                                             "address_ru": "string",
                                             "coordinate": "https://example.com/",
                                         },
                                         200,
                                 ),
                                 (

                                         {
                                             "seo_title": "string",
                                             "seo_description": "string",
                                             "seo_image": {
                                                 "alt": "string",
                                                 "image": Command.create_image_b64('cinema/banner'),
                                                 "filename": 'img.png',
                                             },
                                             "name_uk": "Кінотеатр",
                                             "name_ru": "Кинотеатр",
                                             "description_uk": "string",
                                             "description_ru": "string",
                                             "terms_uk": "{}",
                                             "terms_ru": "{}",
                                             "phone_1": "+380",
                                             "phone_2": "+380",
                                             "email": "user@example.com",
                                             "banner": {
                                                 "alt": "string",
                                                 "image": Command.create_image_b64('cinema/banner'),
                                                 "filename": 'img.jpg',
                                             },
                                             "logo": {
                                                 "alt": "string",
                                                 "image": Command.create_image_b64('cinema/logo'),
                                                 "filename": 'img.svg',
                                             },
                                             "address_uk": "string",
                                             "address_ru": "string",
                                             "coordinate": "https://example.com/",
                                         },
                                         422,
                                 ),
                                 (

                                         {
                                             "seo_title": "string",
                                             "seo_description": "string",
                                             "seo_image": {
                                                 "alt": "string",
                                                 "image": Command.create_image_b64('cinema/banner'),
                                                 "filename": 'img.png',
                                             },
                                             "name_uk": "Кінотеатр-01",
                                             "name_ru": "Кинотеатр-01",
                                             "description_uk": "string",
                                             "description_ru": "string",
                                             "terms_uk": "{}",
                                             "terms_ru": "{}",
                                             "phone_1": "+380985412554",
                                             "phone_2": "+380985412554",
                                             "email": "user@example.com",
                                             "banner": {
                                                 "alt": "string",
                                                 "image": Command.create_image_b64('cinema/banner'),
                                                 "filename": 'img.jpg',
                                             },
                                             "logo": {
                                                 "alt": "string",
                                                 "image": Command.create_image_b64('cinema/logo'),
                                                 "filename": 'img.svg',
                                             },
                                             "address_uk": "string",
                                             "address_ru": "string",
                                             "coordinate": "https://example.com/",
                                         },
                                         409,
                                 )
                             ]
                             )
    def test_create_cinema(self, payload, expected_status):
        response = self.client.post(f"/", json=payload,
                                    headers=self.headers)
        assert response.status_code == expected_status

    @pytest.mark.parametrize("cnm_slug, payload, expected_status",
                             [
                                 (
                                         "knoteatr-01",
                                         {
                                             "seo_title": "string",
                                             "seo_description": "string",
                                             "seo_image": {
                                                 "alt": "string",
                                                 "image": Command.create_image_b64('cinema/banner'),
                                                 "filename": 'img.jpg',
                                             },
                                             "name_uk": "Кінотеатр-01",
                                             "name_ru": "Кинотеатр-01",
                                             "gallery": [
                                                 {
                                                     "alt": "string",
                                                     "image": Command.create_image_b64('cinema/banner'),
                                                     "filename": 'img.jpg',
                                                     "delete": False,
                                                 },
                                                 {
                                                     "alt": "string",
                                                     "image": Command.create_image_b64('cinema/banner'),
                                                     "filename": 'img.jpg',
                                                     "delete": False,
                                                 }
                                             ]
                                         },
                                         200,
                                 ),
                                 (
                                         "knoteatr-010",
                                         {
                                             "name_uk": "Кінотеат-01",
                                             "name_ru": "Кинотеатр-01",
                                         },
                                         409,
                                 ),
                                 (
                                         "knoteatr-010",
                                         {
                                             "phone_1": "+380",
                                         },
                                         422,
                                 ),
                                 (
                                         "knoteatr-010",
                                         {
                                         },
                                         200,
                                 ),
                             ]
                             )
    def test_update_cinema(self, cnm_slug, payload, expected_status):
        response = self.client.patch(f"/{cnm_slug}/", json=payload,
                                     headers=self.headers)
        assert response.status_code == expected_status

    @pytest.mark.parametrize("expected_status",
                             [
                                 200,
                             ]
                             )
    def test_get_all_cinema_cards(self, expected_status):
        response = self.client.get("/all-cards/",
                                   headers=self.headers)
        assert response.status_code == expected_status

    @pytest.mark.parametrize("cnm_slug, expected_status",
                             [
                                 (
                                         "knoteatr-010",
                                         200,
                                 ),
                                 (
                                         "knoteatr-0100",
                                         404,
                                 ),
                             ]
                             )
    def test_delete_cinema(self, cnm_slug, expected_status):
        response = self.client.delete(f"/{cnm_slug}/",
                                      headers=self.headers)
        assert response.status_code == expected_status
