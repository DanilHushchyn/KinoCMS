"""Test cases for core essences(Gallery, Image)"""

import pytest
from ninja_extra.testing import TestClient

from .endpoints.gallery import GalleryController
from .endpoints.statistic import StatisticController


@pytest.mark.django_db()
class TestGalleryController:
    headers = {"Authorization": "Bearer admin"}
    client = TestClient(GalleryController)

    @pytest.mark.parametrize(
        "gallery_id, expected_status",
        [
            (
                1,
                200,
            ),
            (
                111111111,
                404,
            ),
        ],
    )
    def test_get_gallery(self, gallery_id, expected_status):
        response = self.client.get(f"/{gallery_id}/", headers=self.headers)
        assert response.status_code == expected_status


@pytest.mark.django_db()
class TestStatisticController:
    headers = {"Authorization": "Bearer admin"}
    client = TestClient(StatisticController)

    def test_get_computed_nums(self):
        response = self.client.get("/computed_nums/", headers=self.headers)
        assert response.status_code == 200

    def test_get_most_popular_movies(self):
        response = self.client.get("/most-popular-movies/", headers=self.headers)
        assert response.status_code == 200

    def test_get_most_income_movies(self):
        response = self.client.get("/most-income-movies/", headers=self.headers)
        assert response.status_code == 200

    def test_get_most_popular_techs(self):
        response = self.client.get("/most-popular-techs/", headers=self.headers)
        assert response.status_code == 200
