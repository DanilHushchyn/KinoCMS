"""Testing module for authorization"""

import json

import pytest
from ninja_extra.testing import TestClient
from pydantic_core._pydantic_core import ValidationError

from ..core.schemas.base import MessageOutSchema
from .endpoints import CustomTokenObtainPairController
from .test_schemas import UserTestOutSchema


@pytest.mark.django_db()
class TestCustomTokenObtainPairController:
    headers = {"Authorization": "Bearer admin"}
    client = TestClient(CustomTokenObtainPairController)

    def test_get_cities(self):
        response = self.client.get("/cities/choices/")
        assert response.status_code == 200

    def test_get_profile(self):
        response = self.client.get("/my-profile/", headers=self.headers)
        response_encoded = json.dumps(response.json(), ensure_ascii=False)
        result = UserTestOutSchema.model_validate_json(response_encoded)
        assert bool(result) is True
        assert response.status_code == 200

    @pytest.mark.parametrize(
        "payload,expected_status",
        [
            (
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
                {
                    "first_name": "jack",
                },
                422,
            ),
            (
                {
                    "password": "sword123",
                },
                422,
            ),
            (
                {
                    "birthday": "birthday",
                },
                422,
            ),
            (
                {
                    "city": "неизвестно",
                },
                422,
            ),
            (
                {
                    "email": "email",
                },
                422,
            ),
            (
                {
                    "phone_number": "+3809867",
                },
                422,
            ),
        ],
    )
    def test_update_my_profile(self, payload, expected_status):
        response = self.client.patch("/my-profile/", json=payload, headers=self.headers)
        assert response.status_code == expected_status

        if response.status_code == 200:
            try:
                response_encoded = json.dumps(response.json(), ensure_ascii=False)
                UserTestOutSchema.model_validate_json(response_encoded)
            except ValidationError:
                assert False
            if "password" in payload:
                del payload["password"]
            for key in payload.keys():
                assert payload[key] == response.json()[key]

    @pytest.mark.parametrize(
        "payload,expected_status",
        [
            (
                {
                    "first_name": "Данил",
                    "last_name": "Гущин",
                    "nickname": "string",
                    "man": True,
                    "phone_number": "+380985671324",
                    "email": "custom@example.com",
                    "address": "string",
                    "city": "інше",
                    "birthday": "12.12.2012",
                    "password1": "Sword123*",
                    "password2": "Sword123*",
                },
                200,
            ),
            (
                {
                    "first_name": "Данил",
                    "last_name": "Гущин",
                    "nickname": "string",
                    "man": True,
                    "phone_number": "+3809856",
                    "email": "custom@example.com",
                    "address": "string",
                    "city": "інше",
                    "birthday": "12.12.2012",
                    "password1": "Sword123*",
                    "password2": "Sword123*",
                },
                422,
            ),
            (
                {},
                422,
            ),
            (
                {
                    "first_name": "Данил",
                    "last_name": "Гущин",
                    "nickname": "string",
                    "man": True,
                    "phone_number": "+380985645623",
                    "email": "custom@example.com",
                    "address": "string",
                    "city": "інше",
                    "birthday": "birthday",
                    "password1": "Sword123*",
                    "password2": "Sword123*",
                },
                422,
            ),
            (
                {
                    "first_name": "Данил",
                    "last_name": "Гущин",
                    "nickname": "string",
                    "man": True,
                    "phone_number": "+380985645623",
                    "email": "example.com",
                    "address": "string",
                    "city": "інше",
                    "birthday": "12.12.2012",
                    "password1": "Sword123*",
                    "password2": "Sword123*",
                },
                422,
            ),
            (
                {
                    "first_name": "Данил",
                    "last_name": "Гущин",
                    "nickname": "string",
                    "man": True,
                    "phone_number": "+380985645623",
                    "email": "custom@example.com",
                    "address": "string",
                    "city": "інше",
                    "birthday": "12.12.2012",
                    "password1": "Sword123*",
                    "password2": "Sword321*",
                },
                422,
            ),
        ],
    )
    def test_register(self, payload, expected_status):
        response = self.client.post("/register/", json=payload, headers=self.headers)
        assert response.status_code == expected_status

        if response.status_code == 200:
            try:
                response_encoded = json.dumps(response.json(), ensure_ascii=False)
                MessageOutSchema.model_validate_json(response_encoded)
            except ValidationError:
                assert False

    @pytest.mark.parametrize(
        "payloads,expected_status",
        [
            (
                [
                    {
                        "first_name": "Данил",
                        "last_name": "Гущин",
                        "nickname": "nickname",
                        "man": True,
                        "phone_number": "+380985671324",
                        "email": "custom@example.com",
                        "address": "string",
                        "city": "інше",
                        "birthday": "12.12.2012",
                        "password1": "Sword123*",
                        "password2": "Sword123*",
                    },
                    {
                        "first_name": "Данил",
                        "last_name": "Гущин",
                        "nickname": "nickname",
                        "man": True,
                        "phone_number": "+380985671324",
                        "email": "custom@example.com",
                        "address": "string",
                        "city": "інше",
                        "birthday": "12.12.2012",
                        "password1": "Sword123*",
                        "password2": "Sword123*",
                    },
                ],
                409,
            ),
        ],
    )
    def test_register_conflict(self, payloads, expected_status):
        for payload in payloads:
            response = self.client.post(
                "/register/", json=payload, headers=self.headers
            )

        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "payload,expected_status",
        [
            (
                {
                    "email": "user@example.com",
                    "password": "Sword123*",
                },
                200,
            ),
            (
                {
                    "email": "unknown@example.com",
                    "password": "Sword123*",
                },
                401,
            ),
            (
                {
                    "email": "user@example.com",
                },
                400,
            ),
            (
                {
                    "password": "Sword123*",
                },
                400,
            ),
        ],
    )
    def test_login(self, payload, expected_status):
        response = self.client.post(
            "/login",
            json=payload,
        )

        assert response.status_code == expected_status
