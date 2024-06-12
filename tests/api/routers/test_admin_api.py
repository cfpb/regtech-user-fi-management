from unittest.mock import Mock

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from starlette.authentication import AuthCredentials

from regtech_api_commons.models.auth import RegTechUser, AuthenticatedUser


class TestAdminApi:
    def test_get_me_unauthed(self, app_fixture: FastAPI, unauthed_user_mock: Mock):
        client = TestClient(app_fixture)
        res = client.get("/v1/admin/me")
        assert res.status_code == 403

    def test_get_me_authed(self, mocker: MockerFixture, app_fixture: FastAPI, authed_user_mock: Mock):
        get_user_mock = mocker.patch("regtech_api_commons.oauth2.oauth2_admin.OAuth2Admin.get_user")
        get_user_mock.return_value = authed_user_mock.return_value[1]
        client = TestClient(app_fixture)
        res = client.get("/v1/admin/me")
        get_user_mock.assert_called_once_with("testuser123")
        assert res.status_code == 200
        assert res.json().get("name") == "test"
        assert res.json().get("institutions") == []

    def test_get_me_authed_with_institutions(self, mocker: MockerFixture, app_fixture: FastAPI, auth_mock: Mock):
        claims = {
            "name": "test",
            "preferred_username": "test_user",
            "email": "test@local.host",
            "sub": "testuser123",
            "institutions": ["/TEST1LEI100000000000", "/TEST2LEI200000000000/TEST2CHILDLEI1000000"],
        }
        auth_mock.return_value = (
            AuthCredentials(["authenticated"]),
            AuthenticatedUser.from_claim(claims),
        )
        get_user_mock = mocker.patch("regtech_api_commons.oauth2.oauth2_admin.OAuth2Admin.get_user")
        get_user_mock.return_value = RegTechUser.from_claim(claims)
        client = TestClient(app_fixture)
        res = client.get("/v1/admin/me")
        assert res.status_code == 200
        assert res.json().get("institutions") == ["TEST1LEI100000000000", "TEST2CHILDLEI1000000"]

    def test_update_me_unauthed(self, app_fixture: FastAPI, unauthed_user_mock: Mock):
        client = TestClient(app_fixture)
        res = client.put(
            "/v1/admin/me", json={"first_name": "testFirst", "last_name": "testLast", "leis": ["TEST1LEI100000000000"]}
        )
        assert res.status_code == 403

    def test_update_me_no_permission(self, app_fixture: FastAPI, auth_mock: Mock):
        claims = {
            "name": "test",
            "preferred_username": "test_user",
            "email": "test@local.host",
            "sub": "testuser123",
        }
        auth_mock.return_value = (
            AuthCredentials(["authenticated"]),
            AuthenticatedUser.from_claim(claims),
        )
        client = TestClient(app_fixture)
        res = client.put(
            "/v1/admin/me", json={"first_name": "testFirst", "last_name": "testLast", "leis": ["TEST1LEI100000000000"]}
        )
        assert res.status_code == 403

    def test_update_me(self, mocker: MockerFixture, app_fixture: FastAPI, auth_mock: Mock):
        update_user_mock = mocker.patch("regtech_api_commons.oauth2.oauth2_admin.OAuth2Admin.update_user")
        associate_lei_mock = mocker.patch("regtech_api_commons.oauth2.oauth2_admin.OAuth2Admin.associate_to_leis")
        get_user_mock = mocker.patch("regtech_api_commons.oauth2.oauth2_admin.OAuth2Admin.get_user")
        claims = {
            "name": "testFirst testLast",
            "preferred_username": "test_user",
            "email": "test@local.host",
            "sub": "testuser123",
            "institutions": ["TEST1LEI100000000000", "TEST2LEI200000000000"],
        }
        auth_mock.return_value = (
            AuthCredentials(["manage-account"]),
            AuthenticatedUser.from_claim(claims),
        )
        update_user_mock.return_value = None
        associate_lei_mock.return_value = None
        get_user_mock.return_value = auth_mock.return_value[1]
        client = TestClient(app_fixture)
        data = {
            "first_name": "testFirst",
            "last_name": "testLast",
            "leis": ["TEST1LEI100000000000", "TEST2LEI200000000000"],
        }
        res = client.put("/v1/admin/me", json=data)
        update_user_mock.assert_called_once_with("testuser123", {"firstName": "testFirst", "lastName": "testLast"})
        associate_lei_mock.assert_called_once_with("testuser123", {"TEST1LEI100000000000", "TEST2LEI200000000000"})
        assert res.status_code == 200
        assert res.json().get("name") == "testFirst testLast"
        assert res.json().get("institutions") == ["TEST1LEI100000000000", "TEST2LEI200000000000"]

    def test_update_me_no_lei(self, mocker: MockerFixture, app_fixture: FastAPI, auth_mock: Mock):
        update_user_mock = mocker.patch("regtech_api_commons.oauth2.oauth2_admin.OAuth2Admin.update_user")
        associate_lei_mock = mocker.patch("regtech_api_commons.oauth2.oauth2_admin.OAuth2Admin.associate_to_leis")
        get_user_mock = mocker.patch("regtech_api_commons.oauth2.oauth2_admin.OAuth2Admin.get_user")
        claims = {
            "name": "testFirst testLast",
            "preferred_username": "test_user",
            "email": "test@local.host",
            "sub": "testuser123",
        }
        auth_mock.return_value = (
            AuthCredentials(["manage-account"]),
            AuthenticatedUser.from_claim(claims),
        )
        update_user_mock.return_value = None
        get_user_mock.return_value = auth_mock.return_value[1]
        client = TestClient(app_fixture)
        res = client.put("/v1/admin/me", json={"first_name": "testFirst", "last_name": "testLast"})
        update_user_mock.assert_called_once_with("testuser123", {"firstName": "testFirst", "lastName": "testLast"})
        associate_lei_mock.assert_not_called()
        assert res.status_code == 200
        assert res.json().get("name") == "testFirst testLast"
        assert res.json().get("institutions") == []

    def test_associate_institutions(self, mocker: MockerFixture, app_fixture: FastAPI, auth_mock: Mock):
        associate_lei_mock = mocker.patch("regtech_api_commons.oauth2.oauth2_admin.OAuth2Admin.associate_to_leis")
        get_user_mock = mocker.patch("regtech_api_commons.oauth2.oauth2_admin.OAuth2Admin.get_user")
        claims = {
            "name": "test",
            "preferred_username": "test_user",
            "email": "test@local.host",
            "sub": "testuser123",
            "institutions": ["TEST1LEI100000000000", "TEST2LEI200000000000"],
        }
        auth_mock.return_value = (
            AuthCredentials(["manage-account"]),
            AuthenticatedUser.from_claim(claims),
        )
        associate_lei_mock.return_value = None
        get_user_mock.return_value = auth_mock.return_value[1]
        client = TestClient(app_fixture)
        res = client.put("/v1/admin/me/institutions", json=["TEST1LEI100000000000", "TEST2LEI200000000000"])
        associate_lei_mock.assert_called_once_with("testuser123", {"TEST1LEI100000000000", "TEST2LEI200000000000"})
        assert res.status_code == 200
        assert res.json().get("name") == "test"
        assert res.json().get("institutions") == ["TEST1LEI100000000000", "TEST2LEI200000000000"]
