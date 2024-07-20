"""Test cases for movie app"""

import pytest
from ninja_extra.testing import TestClient

from ..core.management.commands.init_script import Command
from .endpoints import MovieController


@pytest.mark.django_db()
class TestCinemaAdminController:
    headers = {"Authorization": "Bearer admin"}
    client = TestClient(MovieController)

    @pytest.mark.parametrize(
        "mv_slug,expected_status",
        [
            (
                "movie-01",
                200,
            ),
            (
                "movie-00",
                404,
            ),
        ],
    )
    def test_get_movie(self, mv_slug, expected_status):
        response = self.client.get(f"/{mv_slug}/", headers=self.headers)
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
                        "image": Command.create_image_b64("movie/card"),
                        "filename": "img.jpg",
                    },
                    "name_uk": "Фільм",
                    "name_ru": "Фільм",
                    "description_uk": "string",
                    "description_ru": "string",
                    "trailer_link": "https://example.com/",
                    "year": 2010,
                    "budget": 700000,
                    "legal_age": "+0",
                    "duration": "01:30",
                    "participants": [1, 2],
                    "techs": [1],
                    "released": "12.12.2024",
                    "genres": ["comedy"],
                    "countries": ["AF"],
                    "card_img": {
                        "alt": "string",
                        "image": Command.create_image_b64("movie/card"),
                        "filename": "img.jpg",
                    },
                },
                200,
            ),
            (
                # Технологии с таким id нету в базе
                {
                    "seo_title": "string",
                    "seo_description": "string",
                    "seo_image": {
                        "alt": "string",
                        "image": Command.create_image_b64("movie/card"),
                        "filename": "img.jpg",
                    },
                    "trailer_link": "https://example.com/",
                    "year": 2010,
                    "budget": 700000,
                    "legal_age": "+0",
                    "duration": "01:30",
                    "participants": [1, 2],
                    "techs": [0],
                    "released": "12.12.2024",
                    "genres": ["comedy"],
                    "countries": ["AF"],
                    "name_uk": "Фільм",
                    "name_ru": "Фільм",
                    "description_uk": "string",
                    "description_ru": "string",
                    "card_img": {
                        "alt": "string",
                        "image": Command.create_image_b64("movie/card"),
                        "filename": "img.jpg",
                    },
                },
                404,
            ),
            (
                # Participant с таким id нету в базе
                {
                    "seo_title": "string",
                    "seo_description": "string",
                    "seo_image": {
                        "alt": "string",
                        "image": Command.create_image_b64("movie/card"),
                        "filename": "img.jpg",
                    },
                    "trailer_link": "https://example.com/",
                    "year": 2010,
                    "budget": 700000,
                    "legal_age": "+0",
                    "duration": "01:30",
                    "participants": [0],
                    "techs": [1],
                    "released": "12.12.2024",
                    "genres": ["comedy"],
                    "countries": ["AF"],
                    "name_uk": "Фільм",
                    "name_ru": "Фільм",
                    "description_uk": "string",
                    "description_ru": "string",
                    "card_img": {
                        "alt": "string",
                        "image": Command.create_image_b64("movie/card"),
                        "filename": "img.jpg",
                    },
                },
                404,
            ),
            (
                # Жанр с таким ключом не существует
                {
                    "seo_title": "string",
                    "seo_description": "string",
                    "seo_image": {
                        "alt": "string",
                        "image": Command.create_image_b64("movie/card"),
                        "filename": "img.jpg",
                    },
                    "trailer_link": "https://example.com/",
                    "year": 2010,
                    "budget": 700000,
                    "legal_age": "+0",
                    "duration": "01:30",
                    "participants": [1],
                    "techs": [1],
                    "released": "12.12.2024",
                    "genres": ["genre"],
                    "countries": ["AF"],
                    "name_uk": "Фільм",
                    "name_ru": "Фільм",
                    "description_uk": "string",
                    "description_ru": "string",
                    "card_img": {
                        "alt": "string",
                        "image": Command.create_image_b64("movie/card"),
                        "filename": "img.jpg",
                    },
                },
                422,
            ),
            (
                # Страна с таким ключом не существует
                {
                    "seo_title": "string",
                    "seo_description": "string",
                    "seo_image": {
                        "alt": "string",
                        "image": Command.create_image_b64("movie/card"),
                        "filename": "img.jpg",
                    },
                    "trailer_link": "https://example.com/",
                    "year": 2010,
                    "budget": 700000,
                    "legal_age": "+0",
                    "duration": "01:30",
                    "participants": [1],
                    "techs": [1],
                    "released": "12.12.2024",
                    "genres": ["comedy"],
                    "countries": ["anonym"],
                    "name_uk": "Фільм",
                    "name_ru": "Фільм",
                    "description_uk": "string",
                    "description_ru": "string",
                    "card_img": {
                        "alt": "string",
                        "image": Command.create_image_b64("movie/card"),
                        "filename": "img.jpg",
                    },
                },
                422,
            ),
            (
                # Legal age с таким ключом не существует
                {
                    "seo_title": "string",
                    "seo_description": "string",
                    "seo_image": {
                        "alt": "string",
                        "image": Command.create_image_b64("movie/card"),
                        "filename": "img.jpg",
                    },
                    "trailer_link": "https://example.com/",
                    "year": 2010,
                    "budget": 700000,
                    "legal_age": "+200",
                    "duration": "01:30",
                    "participants": [1],
                    "techs": [1],
                    "released": "12.12.2024",
                    "genres": ["comedy"],
                    "countries": ["LI"],
                    "name_uk": "Фільм",
                    "name_ru": "Фільм",
                    "description_uk": "string",
                    "description_ru": "string",
                    "card_img": {
                        "alt": "string",
                        "image": Command.create_image_b64("movie/card"),
                        "filename": "img.jpg",
                    },
                },
                422,
            ),
            (
                # Дата релиза от сегодняшнего дня должна отталкиваться
                {
                    "seo_title": "string",
                    "seo_description": "string",
                    "seo_image": {
                        "alt": "string",
                        "image": Command.create_image_b64("movie/card"),
                        "filename": "img.jpg",
                    },
                    "trailer_link": "https://example.com/",
                    "year": 2010,
                    "budget": 700000,
                    "legal_age": "+18",
                    "duration": "01:30",
                    "participants": [1],
                    "techs": [1],
                    "released": "12.12.2020",
                    "genres": ["comedy"],
                    "countries": ["LI"],
                    "name_uk": "Фільм",
                    "name_ru": "Фільм",
                    "description_uk": "string",
                    "description_ru": "string",
                    "card_img": {
                        "alt": "string",
                        "image": Command.create_image_b64("movie/card"),
                        "filename": "img.jpg",
                    },
                },
                422,
            ),
            (
                {
                    "seo_title": "string",
                    "seo_description": "string",
                    "seo_image": {
                        "alt": "string",
                        "image": Command.create_image_b64("movie/card"),
                        "filename": "img.jpg",
                    },
                    "name_uk": "Фільм-01",
                    "name_ru": "Фільм-01",
                    "description_uk": "string",
                    "description_ru": "string",
                    "trailer_link": "https://example.com/",
                    "year": 2010,
                    "budget": 700000,
                    "legal_age": "+0",
                    "duration": "01:30",
                    "participants": [1],
                    "techs": [1],
                    "released": "12.12.2024",
                    "genres": ["comedy"],
                    "countries": ["LI"],
                    "card_img": {
                        "alt": "string",
                        "image": Command.create_image_b64("movie/card"),
                        "filename": "img.jpg",
                    },
                },
                409,
            ),
        ],
    )
    def test_create_movie(self, payload, expected_status):
        response = self.client.post("/", json=payload, headers=self.headers)
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "mv_slug, payload, expected_status",
        [
            (
                "movie-01",
                {
                    "seo_title": "string",
                    "seo_description": "string",
                    "seo_image": {
                        "alt": "string",
                        "image": Command.create_image_b64("movie/card"),
                        "filename": "img.jpg",
                    },
                    "name_uk": "Фільм-01",
                    "name_ru": "Фильм-01",
                    "gallery": [
                        {
                            "alt": "string",
                            "image": Command.create_image_b64("movie/card"),
                            "filename": "img.jpg",
                            "delete": False,
                        },
                        {
                            "alt": "string",
                            "image": Command.create_image_b64("movie/card"),
                            "filename": "img.jpg",
                            "delete": False,
                        },
                    ],
                },
                200,
            ),
            (
                "movie-010",
                {
                    "name_uk": "Фільм-01",
                    "name_ru": "Фильм-01",
                },
                409,
            ),
            (
                "movie-010",
                {
                    "genres": ["unknown"],
                },
                422,
            ),
            (
                "movie-010",
                {
                    "countries": ["xxx"],
                },
                422,
            ),
            (
                "movie-010",
                {"legal_age": "200"},
                422,
            ),
            (
                "movie-010",
                {"year": 200},
                422,
            ),
            (
                "movie-010",
                {
                    "participants": [0],
                },
                404,
            ),
            (
                "movie-010",
                {},
                200,
            ),
        ],
    )
    def test_update_movie(self, mv_slug, payload, expected_status):
        response = self.client.patch(f"/{mv_slug}/", json=payload, headers=self.headers)
        assert response.status_code == expected_status

    def test_get_all_movie_cards(self):
        response = self.client.get("/all-cards/", headers=self.headers)
        assert response.status_code == 200

    def test_get_all_movie_techs(self):
        response = self.client.get("/techs/", headers=self.headers)
        assert response.status_code == 200

    def test_get_all_movie_participants(self):
        response = self.client.get("/participants/", headers=self.headers)
        assert response.status_code == 200

    def test_get_all_movie_participants_grouped(self):
        response = self.client.get("/participants-grouped/", headers=self.headers)
        assert response.status_code == 200

    def test_get_all_movie_countries(self):
        response = self.client.get("/countries/", headers=self.headers)
        assert response.status_code == 200

    def test_get_all_movie_genres(self):
        response = self.client.get("/genres/", headers=self.headers)
        assert response.status_code == 200

    def test_get_all_movie_legal_ages(self):
        response = self.client.get("/legal-ages/", headers=self.headers)
        assert response.status_code == 200

    @pytest.mark.parametrize(
        "mv_slug, expected_status",
        [
            (
                "movie-010",
                200,
            ),
            (
                "knoteatr-0100",
                404,
            ),
        ],
    )
    def test_delete_movie(self, mv_slug, expected_status):
        response = self.client.delete(f"/{mv_slug}/", headers=self.headers)
        assert response.status_code == expected_status
