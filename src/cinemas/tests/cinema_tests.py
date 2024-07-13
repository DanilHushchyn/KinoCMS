import json

import pytest
from ninja_extra.testing import TestClient
from ..endpoints.cinema import CinemaController


@pytest.mark.django_db
class TestCinemaAdminController:
    headers = {
        'Authorization': 'Bearer admin'
    }
    client = TestClient(CinemaController)

    @pytest.mark.parametrize("user_id,expected_status",
                             [
                                 (

                                         1,
                                         200,
                                 ),
                             ]
                             )
    def test_create_cinema(self, user_id, expected_status):
        response = self.client.get("/knoteatr-01/",
                                    headers=self.headers)
        print(response.status_code)
        print(response.json())
        # assert response.status_code == expected_status
        # if response.status_code == 200:
        #     response_encoded = json.dumps(response.json(), ensure_ascii=False)
        #     result = MessageOutSchema.model_validate_json(response_encoded)
        #     assert bool(result) is True
