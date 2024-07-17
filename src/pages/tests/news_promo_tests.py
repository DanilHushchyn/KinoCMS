import pytest
from ninja_extra.testing import TestClient
import src.pages.endpoints.news_promo as np
import src.core.management.commands.init_script as init


@pytest.mark.django_db
class TestNewsPromoController:
    headers = {
        'Authorization': 'Bearer admin'
    }
    client = TestClient(np.NewsPromoController)

    @pytest.mark.parametrize("np_slug,expected_status",
                             [
                                 (

                                         "aktsya-02",
                                         200,
                                 ),
                                 (

                                         "aktsya-20000",
                                         404,
                                 ),
                                 (

                                         "novina-07",
                                         200,
                                 ),
                                 (

                                         "novina-70000",
                                         404,
                                 ),
                             ]
                             )
    def test_get_news_promo(self, np_slug, expected_status):
        response = self.client.get(f"/{np_slug}/",
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
                                                 "image": init.Command.create_image_b64('movie/card'),
                                                 "filename": 'img.jpg',
                                             },
                                             "banner": {
                                                 "alt": "string",
                                                 "image": init.Command.create_image_b64('movie/card'),
                                                 "filename": 'img.jpg',
                                             },
                                             "name_uk": "Новина",
                                             "name_ru": "Новость",
                                             "description_uk": "{}",
                                             "description_ru": "{}",
                                             "video_link": "https://example.com/",
                                             "active": True,
                                             "promo": True,
                                             "tags": [
                                                 1, 2
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
                                                 "image": init.Command.create_image_b64('movie/card'),
                                                 "filename": 'img.jpg',
                                             },
                                             "banner": {
                                                 "alt": "string",
                                                 "image": init.Command.create_image_b64('movie/card'),
                                                 "filename": 'img.jpg',
                                             },
                                             "name_uk": "Новина - 05",
                                             "name_ru": "Новость - 05",
                                             "description_uk": "{}",
                                             "description_ru": "{}",
                                             "video_link": "https://example.com/",
                                             "active": True,
                                             "promo": True,
                                             "tags": [
                                                 1, 2
                                             ]
                                         },
                                         409,
                                 ),

                             ]
                             )
    def test_create_news_promo(self, payload, expected_status):
        response = self.client.post(f"/", json=payload,
                                    headers=self.headers)
        assert response.status_code == expected_status

    def test_get_all_news_promo_cards(self):
        response = self.client.get("/all-cards/?promo=true",
                                   headers=self.headers)
        assert response.status_code == 200
        response = self.client.get("/all-cards/?promo=false",
                                   headers=self.headers)
        assert response.status_code == 200

    def test_get_all_news_promo_tags(self):
        response = self.client.get("/all-tags/",
                                   headers=self.headers)
        assert response.status_code == 200

    @pytest.mark.parametrize("np_slug, payload, expected_status",
                             [
                                 (
                                         "novina-05",
                                         {
                                             "seo_title": "string",
                                             "seo_description": "string",
                                             "seo_image": {
                                                 "alt": "string",
                                                 "image": init.Command.create_image_b64('movie/card'),
                                                 "filename": 'img.jpg',
                                             },
                                             "banner": {
                                                 "alt": "string",
                                                 "image": init.Command.create_image_b64('movie/card'),
                                                 "filename": 'img.jpg',
                                             },
                                             "name_uk": "Новина - 05",
                                             "name_ru": "Новость - 05",
                                             "description_uk": "{}",
                                             "description_ru": "{}",
                                             "video_link": "https://example.com/",
                                             "active": True,
                                             "promo": True,
                                             "tags": [
                                                 1, 2
                                             ]
                                         },
                                         200,
                                 ),
                                 (
                                         "novina-05",
                                         {

                                         },
                                         200,
                                 ),
                                 (
                                         "novina-05",
                                         {
                                             "seo_title": "string",
                                             "seo_description": "string",
                                             "seo_image": {
                                                 "alt": "string",
                                                 "image": init.Command.create_image_b64('movie/card'),
                                                 "filename": 'img.jpg',
                                             },
                                             "banner": {
                                                 "alt": "string",
                                                 "image": init.Command.create_image_b64('movie/card'),
                                                 "filename": 'img.jpg',
                                             },
                                             "name_uk": "Новина - 07",
                                             "name_ru": "Новость - 07",
                                             "description_uk": "{}",
                                             "description_ru": "{}",
                                             "video_link": "https://example.com/",
                                             "active": True,
                                             "promo": True,
                                             "tags": [
                                                 1, 2
                                             ]
                                         },
                                         409,
                                 ),

                             ]
                             )
    def test_update_news_promo(self, np_slug, payload, expected_status):
        response = self.client.patch(f"/{np_slug}/", json=payload,
                                     headers=self.headers)
        assert response.status_code == expected_status

    @pytest.mark.parametrize("np_slug,expected_status",
                             [
                                 (

                                         "novina-05",
                                         200,
                                 ),
                                 (

                                         "novina-00",
                                         404,
                                 ),
                             ]
                             )
    def test_delete_news_promo(self, np_slug, expected_status):
        response = self.client.delete(f"/{np_slug}/",
                                      headers=self.headers)
        assert response.status_code == expected_status
