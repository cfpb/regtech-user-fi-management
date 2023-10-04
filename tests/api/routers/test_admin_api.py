from unittest.mock import Mock

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from starlette.authentication import AuthCredentials

from entities.models import AuthenticatedUser


class TestAdminApi:
    def test_get_me_unauthed(self, app_fixture: FastAPI, unauthed_user_mock: Mock):
        client = TestClient(app_fixture)
        res = client.get("/v1/admin/me")
        assert res.status_code == 403

    def test_get_me_authed(self, mocker: MockerFixture, app_fixture: FastAPI, authed_user_mock: Mock):
        client = TestClient(app_fixture)
        res = client.get("/v1/admin/me")
        assert res.status_code == 200
        assert res.json().get("name") == "test"
        assert res.json().get("institutions") == []

    def test_get_me_authed_with_institutions(self, app_fixture: FastAPI, auth_mock: Mock):
        claims = {
            "name": "test",
            "preferred_username": "test_user",
            "email": "test@local.host",
            "sub": "testuser123",
            "institutions": ["/TEST1LEI", "/TEST2LEI/TEST2CHILDLEI"],
        }
        auth_mock.return_value = (
            AuthCredentials(["authenticated"]),
            AuthenticatedUser.from_claim(claims),
        )
        client = TestClient(app_fixture)
        res = client.get("/v1/admin/me")
        assert res.status_code == 200
        assert res.json().get("institutions") == ["TEST1LEI", "TEST2CHILDLEI"]

    def test_update_me_unauthed(self, app_fixture: FastAPI, unauthed_user_mock: Mock):
        client = TestClient(app_fixture)
        res = client.put("/v1/admin/me", json={"first_name": "testFirst", "last_name": "testLast", "leis": ["testLei"]})
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
        res = client.put("/v1/admin/me", json={"first_name": "testFirst", "last_name": "testLast", "leis": ["testLei"]})
        assert res.status_code == 403

    def test_update_me(self, mocker: MockerFixture, app_fixture: FastAPI, authed_user_mock: Mock):
        update_user_mock = mocker.patch("oauth2.oauth2_admin.OAuth2Admin.update_user")
        associate_lei_mock = mocker.patch("oauth2.oauth2_admin.OAuth2Admin.associate_to_leis")
        update_user_mock.return_value = None
        associate_lei_mock.return_value = None
        client = TestClient(app_fixture)
        data = {"first_name": "testFirst", "last_name": "testLast", "leis": ["testLei1", "testLei2"]}
        res = client.put("/v1/admin/me", json=data)
        update_user_mock.assert_called_once_with("testuser123", {"firstName": "testFirst", "lastName": "testLast"})
        associate_lei_mock.assert_called_once_with("testuser123", {"testLei1", "testLei2"})
        assert res.status_code == 202

    def test_update_me_no_lei(self, mocker: MockerFixture, app_fixture: FastAPI, authed_user_mock: Mock):
        update_user_mock = mocker.patch("oauth2.oauth2_admin.OAuth2Admin.update_user")
        associate_lei_mock = mocker.patch("oauth2.oauth2_admin.OAuth2Admin.associate_to_leis")
        update_user_mock.return_value = None
        client = TestClient(app_fixture)
        res = client.put("/v1/admin/me", json={"first_name": "testFirst", "last_name": "testLast"})
        update_user_mock.assert_called_once_with("testuser123", {"firstName": "testFirst", "lastName": "testLast"})
        associate_lei_mock.assert_not_called()
        assert res.status_code == 202

    def test_associate_institutions(self, mocker: MockerFixture, app_fixture: FastAPI, authed_user_mock: Mock):
        associate_lei_mock = mocker.patch("oauth2.oauth2_admin.OAuth2Admin.associate_to_leis")
        associate_lei_mock.return_value = None
        client = TestClient(app_fixture)
        res = client.put("/v1/admin/me/institutions", json=["testlei1", "testlei2"])
        associate_lei_mock.assert_called_once_with("testuser123", {"testlei1", "testlei2"})
        assert res.status_code == 202
