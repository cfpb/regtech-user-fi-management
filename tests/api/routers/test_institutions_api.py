from unittest.mock import Mock

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from starlette.authentication import AuthCredentials
from oauth2.oauth2_backend import AuthenticatedUser
from entities.models import (
    FinancialInstitutionDao,
    FinancialInstitutionDomainDao
)


class TestInstitutionsApi:
    def test_get_institutions_unauthed(self, app_fixture: FastAPI, unauthed_user_mock: Mock):
        client = TestClient(app_fixture)
        res = client.get("/v1/institutions/")
        assert res.status_code == 403

    def test_get_institutions_authed(
        self, mocker: MockerFixture, app_fixture: FastAPI, authed_user_mock: Mock
    ):
        get_institutions_mock = mocker.patch("entities.repos.institutions_repo.get_institutions")
        get_institutions_mock.return_value = [FinancialInstitutionDao(
            name="Test Bank 123",
            lei="TESTBANK123",
            domains=[
                FinancialInstitutionDomainDao(domain="test.bank", lei="TESTBANK123")
            ],
        )]
        client = TestClient(app_fixture)
        res = client.get("/v1/institutions/")
        assert res.status_code == 200
        assert res.json()[0].get("name") == "Test Bank 123"

    def test_create_institution_unauthed(self, app_fixture: FastAPI, unauthed_user_mock: Mock):
        client = TestClient(app_fixture)
        res = client.post("/v1/institutions/", json={"name": "testName", "lei": "testLei"})
        assert res.status_code == 403

    def test_create_institution_authed(self, mocker: MockerFixture, app_fixture: FastAPI, authed_user_mock: Mock):
        upsert_institution_mock = mocker.patch("entities.repos.institutions_repo.upsert_institution")
        upsert_institution_mock.return_value = FinancialInstitutionDao(
            name="testName",
            lei="testLei",
            domains=[
                FinancialInstitutionDomainDao(domain="test.bank", lei="TESTBANK123")
            ],
        )
        upsert_group_mock = mocker.patch("oauth2.oauth2_admin.OAuth2Admin.upsert_group")
        upsert_group_mock.return_value = "leiGroup"
        client = TestClient(app_fixture)
        res = client.post("/v1/institutions/", json={"name": "testName", "lei": "testLei"})
        assert res.status_code == 200
        assert res.json()[1].get("name") == "testName"

    def test_create_institution_authed_no_permission(self, app_fixture: FastAPI, auth_mock: Mock):
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
        res = client.post("/v1/institutions/", json={"name": "testName", "lei": "testLei"})
        assert res.status_code == 403

    def test_get_institution_unauthed(self, app_fixture: FastAPI, unauthed_user_mock: Mock):
        client = TestClient(app_fixture)
        leiPath = "testLeiPath"
        res = client.get(f"/v1/institutions/{leiPath}")
        assert res.status_code == 403

    def test_get_institution_authed(self, mocker: MockerFixture, app_fixture: FastAPI, authed_user_mock: Mock):
        get_institution_mock = mocker.patch("entities.repos.institutions_repo.get_institution")
        get_institution_mock.return_value = FinancialInstitutionDao(
            name="Test Bank 123",
            lei="TESTBANK123",
            domains=[
                FinancialInstitutionDomainDao(domain="test.bank", lei="TESTBANK123")
            ],
        )
        client = TestClient(app_fixture)
        leiPath = "testLeiPath"
        res = client.get(f"/v1/institutions/{leiPath}")
        assert res.status_code == 200
        assert res.json().get("name") == "Test Bank 123"

    def test_add_domains_unauthed(self, app_fixture: FastAPI, unauthed_user_mock: Mock):
        client = TestClient(app_fixture)
        leiPath = "testLeiPath"
        res = client.post(f"/v1/institutions/{leiPath}/domains/", json=[{"domain": "testDomain"}])
        assert res.status_code == 403

    def test_add_domains_authed(self, mocker: MockerFixture, app_fixture: FastAPI, authed_user_mock: Mock):
        add_domains_mock = mocker.patch("entities.repos.institutions_repo.add_domains")
        add_domains_mock.return_value = [FinancialInstitutionDomainDao(domain="test.bank", lei="TESTBANK123")]
        client = TestClient(app_fixture)
        leiPath = "testLeiPath"
        res = client.post(f"/v1/institutions/{leiPath}/domains/", json=[{"domain": "testDomain"}])
        assert res.status_code == 200
        assert res.json()[0].get("domain") == "test.bank"

    def test_add_domains_authed_no_permission(self, app_fixture: FastAPI, auth_mock: Mock):
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
        leiPath = "testLeiPath"
        res = client.post(f"/v1/institutions/{leiPath}/domains/", json=[{"domain": "testDomain"}])
        assert res.status_code == 403