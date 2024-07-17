import pytest
from ninja_extra.testing import TestClient
from .endpoints.gallery import GalleryController


@pytest.mark.django_db
class TestGalleryController:
    headers = {
        'Authorization': 'Bearer admin'
    }
    client = TestClient(GalleryController)

    @pytest.mark.parametrize("gallery_id, expected_status",
                             [
                                 (

                                         1,
                                         200,
                                 ),
                                 (

                                         111111111,
                                         404,
                                 ),
                             ]
                             )
    def test_get_gallery(self, gallery_id, expected_status):
        response = self.client.get(f"/{gallery_id}/",
                                   headers=self.headers)
        assert response.status_code == expected_status
