import json

import pytest
from ninja_extra.testing import TestClient
from pydantic_core._pydantic_core import ValidationError
from ..endpoints import UsersAdminController
from ...authz.test_schemas import UserTestOutSchema
from ...core.schemas.base import MessageOutSchema


@pytest.mark.django_db
class TestUsersAdminController:
    headers = {
        'Authorization': 'Bearer admin'
    }
    client = TestClient(UsersAdminController)

    @pytest.mark.parametrize("user_id,expected_status",
                             [
                                 (

                                         1,
                                         200,
                                 ),
                                 (
                                         11111,
                                         404,
                                 ),
                             ]
                             )
    def test_delete_user_by_id(self, user_id, expected_status):
        response = self.client.delete(f"/detail/{user_id}/",
                                      headers=self.headers)

        assert response.status_code == expected_status
        if response.status_code == 200:
            response_encoded = json.dumps(response.json(), ensure_ascii=False)
            result = MessageOutSchema.model_validate_json(response_encoded)
            assert bool(result) is True

    @pytest.mark.parametrize("payload,expected_status",
                             [
                                 (
                                         {
                                             "user_id": 1,
                                         },
                                         200,
                                 ),
                                 (
                                         {
                                             "user_id": 1111,
                                         },
                                         404,
                                 ),
                             ])
    def test_get_user_by_id(self, payload, expected_status):
        response = self.client.get(f"/detail/{payload['user_id']}/",
                                   headers=self.headers)
        assert response.status_code == expected_status
        if response.status_code == 200:
            response_encoded = json.dumps(response.json(), ensure_ascii=False)
            result = UserTestOutSchema.model_validate_json(response_encoded)
            assert bool(result) is True

    @pytest.mark.parametrize("user_id,payload,expected_status",
                             [
                                 (
                                         1,
                                         {
                                             "first_name": "Данил",
                                             "last_name": "Гущин",
                                             "birthday": "12.12.2012",
                                             "email": "user@example.com",
                                             "phone_number": "+380987661234",
                                         },
                                         200,
                                 ),
                                 (
                                         11,
                                         {
                                             "first_name": "Данил",
                                             "last_name": "Гущин",
                                             "birthday": "12.12.2012",
                                             "email": "user@example.com",
                                             "phone_number": "+380987661234",
                                         },
                                         409,
                                 ),
                                 (
                                         1111,
                                         {
                                             "first_name": "Данил",
                                             "last_name": "Гущин",
                                             "birthday": "12.12.2012",
                                             "email": "user@example.com",
                                             "phone_number": "+380987661234",
                                         },
                                         404,
                                 ),
                                 (
                                         1,
                                         {
                                             "first_name": "jack",
                                         },
                                         422,
                                 ),
                                 (
                                         1,
                                         {
                                             "password": "sword123",
                                         },
                                         422,
                                 ),
                                 (
                                         1,
                                         {
                                             "birthday": "birthday",
                                         },
                                         422,
                                 ),
                                 (
                                         1,
                                         {
                                             "city": "неизвестно",
                                         },
                                         422,
                                 ),
                                 (
                                         1,
                                         {
                                             "email": "email",
                                         },
                                         422,
                                 ),
                                 (
                                         1,
                                         {
                                             "phone_number": "+3809867",
                                         },
                                         422,
                                 ),
                             ]
                             )
    def test_update_user_by_id(self, user_id, payload, expected_status):
        response = self.client.patch(f"/detail/{user_id}/", json=payload,
                                     headers=self.headers)
        assert response.status_code == expected_status

        if response.status_code == 200:
            try:
                response_encoded = json.dumps(response.json(), ensure_ascii=False)
                UserTestOutSchema.model_validate_json(response_encoded)
            except ValidationError:
                assert False
            if 'password' in payload:
                del payload['password']
            for key in payload.keys():
                assert payload[key] == response.json()[key]

    @pytest.mark.parametrize("queries,expected_status",
                             [
                                 (
                                         "?sort=date_joined&direction=descending",
                                         200,
                                 ),
                                 (
                                         "?sort=date_joined&direction=hello",
                                         200,
                                 ),
                                 (
                                         "",
                                         200,
                                 ),
                                 (
                                         "?search_line=12.12.2012",
                                         200,
                                 ),
                                 (
                                         "?sort=hello&direction=descending",
                                         422,
                                 ),
                             ]
                             )
    def test_datable(self, queries, expected_status):
        response = self.client.get(f"/datable/{queries}",
                                   headers=self.headers)
        assert response.status_code == expected_status
