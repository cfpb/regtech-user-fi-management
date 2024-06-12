from http import HTTPStatus
from unittest.mock import Mock, ANY

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from starlette.authentication import AuthCredentials
from regtech_api_commons.models.auth import AuthenticatedUser
from regtech_user_fi_management.entities.models.dao import (
    FinancialInstitutionDao,
    FinancialInstitutionDomainDao,
    FederalRegulatorDao,
    AddressStateDao,
    HMDAInstitutionTypeDao,
    SBLInstitutionTypeDao,
    SblTypeMappingDao,
)
from regtech_user_fi_management.entities.models.dto import SblTypeAssociationDto
from regtech_user_fi_management.config import regex_configs


class TestInstitutionsApi:
    def test_get_institutions_unauthed(self, app_fixture: FastAPI, unauthed_user_mock: Mock):
        client = TestClient(app_fixture)
        res = client.get("/v1/institutions/")
        assert res.status_code == 403

    def test_get_institutions_authed(
        self, mocker: MockerFixture, app_fixture: FastAPI, authed_user_mock: Mock, get_institutions_mock: Mock
    ):
        client = TestClient(app_fixture)
        res = client.get("/v1/institutions/")
        assert res.status_code == 200
        assert res.json()[0].get("name") == "Test Bank 123"

    def test_get_institutions_authed_not_admin(
        self,
        mocker: MockerFixture,
        app_fixture: FastAPI,
        auth_mock: Mock,
    ):
        claims = {
            "name": "test",
            "preferred_username": "test_user",
            "email": "test@local.host",
            "sub": "testuser123",
        }
        auth_mock.return_value = (
            AuthCredentials(["manage-account", "authenticated"]),
            AuthenticatedUser.from_claim(claims),
        )
        client = TestClient(app_fixture)
        res = client.get("/v1/institutions/")
        assert res.status_code == 403

    def test_create_institution_unauthed(self, app_fixture: FastAPI, unauthed_user_mock: Mock):
        client = TestClient(app_fixture)
        res = client.post("/v1/institutions/", json={"name": "testName", "lei": "TESTBANK123000000000"})
        assert res.status_code == 403

    def test_invalid_tax_id(self, mocker: MockerFixture, app_fixture: FastAPI, authed_user_mock: Mock):
        client = TestClient(app_fixture)
        res = client.post(
            "/v1/institutions/",
            json={
                "name": "testName",
                "lei": "TESTBANK123000000000",
                "is_active": True,
                "tax_id": "123456789",
                "rssd_id": 12344,
                "primary_federal_regulator_id": "FRI2",
                "hmda_institution_type_id": "HIT2",
                "sbl_institution_type_ids": ["SIT2"],
                "hq_address_street_1": "Test Address Street 1",
                "hq_address_street_2": "",
                "hq_address_street_3": "",
                "hq_address_street_4": "",
                "hq_address_city": "Test City 1",
                "hq_address_state_code": "VA",
                "hq_address_zip": "00000",
                "parent_lei": "012PARENTTESTBANK123",
                "parent_legal_name": "PARENT TEST BANK 123",
                "parent_rssd_id": 12345,
                "top_holder_lei": "01234TOPHOLDERLEI123",
                "top_holder_legal_name": "TOP HOLDER LEI 123",
                "top_holder_rssd_id": 123456,
            },
        )
        assert f"Value error, Invalid tax_id 123456789. {regex_configs.tin.error_text}" in res.json()["error_detail"]
        assert res.status_code == 422

    def test_invalid_lei(self, mocker: MockerFixture, app_fixture: FastAPI, authed_user_mock: Mock):
        client = TestClient(app_fixture)
        res = client.post(
            "/v1/institutions/",
            json={
                "name": "testName",
                "lei": "test_Lei",
                "is_active": True,
                "tax_id": "12-3456789",
                "rssd_id": 12344,
                "primary_federal_regulator_id": "FRI2",
                "hmda_institution_type_id": "HIT2",
                "sbl_institution_type_ids": ["SIT2"],
                "hq_address_street_1": "Test Address Street 1",
                "hq_address_street_2": "",
                "hq_address_street_3": "",
                "hq_address_street_4": "",
                "hq_address_city": "Test City 1",
                "hq_address_state_code": "VA",
                "hq_address_zip": "00000",
                "parent_lei": "012PARENTTESTBANK123",
                "parent_legal_name": "PARENT TEST BANK 123",
                "parent_rssd_id": 12345,
                "top_holder_lei": "01234TOPHOLDERLEI123",
                "top_holder_legal_name": "TOP HOLDER LEI 123",
                "top_holder_rssd_id": 123456,
            },
        )
        assert f"Value error, Invalid lei test_Lei. {regex_configs.lei.error_text}" in res.json()["error_detail"]
        assert res.status_code == 422

    def test_create_institution_authed(self, mocker: MockerFixture, app_fixture: FastAPI, authed_user_mock: Mock):
        upsert_institution_mock = mocker.patch(
            "regtech_user_fi_management.entities.repos.institutions_repo.upsert_institution"
        )
        upsert_institution_mock.return_value = FinancialInstitutionDao(
            name="testName",
            lei="1234567890ABCDEFGH00",
            is_active=True,
            domains=[FinancialInstitutionDomainDao(domain="test.bank", lei="1234567890ABCDEFGH00")],
            tax_id="12-3456789",
            rssd_id=1234,
            primary_federal_regulator_id="FRI2",
            primary_federal_regulator=FederalRegulatorDao(id="FRI2", name="FRI2"),
            hmda_institution_type_id="HIT2",
            hmda_institution_type=HMDAInstitutionTypeDao(id="HIT2", name="HIT2"),
            sbl_institution_types=[SblTypeMappingDao(sbl_type=SBLInstitutionTypeDao(id="SIT2", name="SIT2"))],
            hq_address_street_1="Test Address Street 1",
            hq_address_street_2="",
            hq_address_street_3="",
            hq_address_street_4="",
            hq_address_city="Test City 1",
            hq_address_state_code="VA",
            hq_address_state=AddressStateDao(code="VA", name="Virginia"),
            hq_address_zip="00000",
            parent_lei="012PARENTTESTBANK123",
            parent_legal_name="PARENT TEST BANK 123",
            parent_rssd_id=12345,
            top_holder_lei="01234TOPHOLDERLEI123",
            top_holder_legal_name="TOP HOLDER LEI 123",
            top_holder_rssd_id=123456,
        )
        upsert_group_mock = mocker.patch("regtech_api_commons.oauth2.oauth2_admin.OAuth2Admin.upsert_group")
        upsert_group_mock.return_value = "leiGroup"
        client = TestClient(app_fixture)
        res = client.post(
            "/v1/institutions/",
            json={
                "name": "testName",
                "lei": "1234567890ABCDEFGH00",
                "is_active": True,
                "tax_id": "12-3456789",
                "rssd_id": 12344,
                "primary_federal_regulator_id": "FRI2",
                "hmda_institution_type_id": "HIT2",
                "sbl_institution_type_ids": ["SIT2"],
                "hq_address_street_1": "Test Address Street 1",
                "hq_address_street_2": "",
                "hq_address_street_3": "",
                "hq_address_street_4": "",
                "hq_address_city": "Test City 1",
                "hq_address_state_code": "VA",
                "hq_address_zip": "00000",
                "parent_lei": "012PARENTTESTBANK123",
                "parent_legal_name": "PARENT TEST BANK 123",
                "parent_rssd_id": 12345,
                "top_holder_lei": "01234TOPHOLDERLEI123",
                "top_holder_legal_name": "TOP HOLDER LEI 123",
                "top_holder_rssd_id": 123456,
            },
        )
        assert res.status_code == 200
        assert res.json()[1].get("name") == "testName"

    def test_create_institution_only_required_fields(
        self, mocker: MockerFixture, app_fixture: FastAPI, authed_user_mock: Mock
    ):
        upsert_institution_mock = mocker.patch(
            "regtech_user_fi_management.entities.repos.institutions_repo.upsert_institution"
        )
        upsert_institution_mock.return_value = FinancialInstitutionDao(
            name="testName",
            lei="1234567890ABCDEFGH00",
            is_active=True,
            hq_address_street_1="Test Address Street 1",
            hq_address_city="Test City 1",
            hq_address_state_code="VA",
            hq_address_state=AddressStateDao(code="VA", name="Virginia"),
            hq_address_zip="00000",
        )
        upsert_group_mock = mocker.patch("regtech_api_commons.oauth2.oauth2_admin.OAuth2Admin.upsert_group")
        upsert_group_mock.return_value = "leiGroup"
        client = TestClient(app_fixture)
        res = client.post(
            "/v1/institutions/",
            json={
                "name": "testName",
                "lei": "1234567890ABCDEFGH00",
                "is_active": True,
                "hq_address_street_1": "Test Address Street 1",
                "hq_address_city": "Test City 1",
                "hq_address_state_code": "VA",
                "hq_address_zip": "00000",
            },
        )
        assert res.status_code == 200
        assert res.json()[1].get("name") == "testName"
        assert res.json()[1].get("tax_id") is None

    def test_create_institution_missing_required_field(
        self, mocker: MockerFixture, app_fixture: FastAPI, authed_user_mock: Mock
    ):
        client = TestClient(app_fixture)
        res = client.post(
            "/v1/institutions/",
            json={
                "name": "testName",
                "lei": "1234567890ABCDEFGH00",
                "hq_address_street_1": "Test Address Street 1",
                "hq_address_city": "Test City 1",
                "hq_address_state_code": "VA",
            },
        )
        assert res.status_code == 422

    def test_create_institution_missing_sbl_type_free_form(
        self, mocker: MockerFixture, app_fixture: FastAPI, authed_user_mock: Mock
    ):
        client = TestClient(app_fixture)
        res = client.post(
            "/v1/institutions/",
            json={
                "name": "testName",
                "lei": "1234567890ABCDEFGH00",
                "is_active": True,
                "hq_address_street_1": "Test Address Street 1",
                "hq_address_city": "Test City 1",
                "hq_address_state_code": "VA",
                "hq_address_zip": "00000",
                "sbl_institution_types": [{"id": "13"}],
            },
        )
        assert res.status_code == 422
        assert "requires additional details." in res.json()["error_detail"]

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
        res = client.post(
            "/v1/institutions/",
            json={
                "name": "testName",
                "lei": "1234567890ABCDEFGH00",
                "is_active": True,
                "tax_id": "12-3456789",
                "rssd_id": 12344,
                "primary_federal_regulator_id": "FIR2",
                "hmda_institution_type_id": "HIT2",
                "sbl_institution_type_ids": ["SIT2"],
                "hq_address_street_1": "Test Address Street 1",
                "hq_address_street_2": "",
                "hq_address_street_3": "",
                "hq_address_street_4": "",
                "hq_address_city": "Test City 1",
                "hq_address_state_code": "VA",
                "hq_address_zip": "00000",
                "parent_lei": "012PARENTTESTBANK123",
                "parent_legal_name": "PARENT TEST BANK 123",
                "parent_rssd_id": 12345,
                "top_holder_lei": "01234TOPHOLDERLEI123",
                "top_holder_legal_name": "TOP HOLDER LEI 123",
                "top_holder_rssd_id": 123456,
            },
        )
        assert res.status_code == 403

    def test_get_institution_unauthed(self, app_fixture: FastAPI, unauthed_user_mock: Mock):
        client = TestClient(app_fixture)
        lei_path = "testLeiPath"
        res = client.get(f"/v1/institutions/{lei_path}")
        assert res.status_code == 403

    def test_get_institution_authed(self, mocker: MockerFixture, app_fixture: FastAPI, authed_user_mock: Mock):
        get_institution_mock = mocker.patch(
            "regtech_user_fi_management.entities.repos.institutions_repo.get_institution"
        )
        get_institution_mock.return_value = FinancialInstitutionDao(
            name="Test Bank 123",
            lei="TESTBANK123000000000",
            is_active=True,
            domains=[FinancialInstitutionDomainDao(domain="test.bank", lei="TESTBANK123000000000")],
            tax_id="12-3456789",
            rssd_id=1234,
            primary_federal_regulator_id="FRI1",
            primary_federal_regulator=FederalRegulatorDao(id="FRI1", name="FRI1"),
            hmda_institution_type_id="HIT1",
            hmda_institution_type=HMDAInstitutionTypeDao(id="HIT1", name="HIT1"),
            sbl_institution_types=[SblTypeMappingDao(sbl_type=SBLInstitutionTypeDao(id="SIT1", name="SIT1"))],
            hq_address_street_1="Test Address Street 1",
            hq_address_street_2="",
            hq_address_street_3="",
            hq_address_street_4="",
            hq_address_city="Test City 1",
            hq_address_state_code="GA",
            hq_address_state=AddressStateDao(code="GA", name="Georgia"),
            hq_address_zip="00000",
            parent_lei="012PARENTTESTBANK123",
            parent_legal_name="PARENT TEST BANK 123",
            parent_rssd_id=12345,
            top_holder_lei="01234TOPHOLDERLEI123",
            top_holder_legal_name="TOP HOLDER LEI 123",
            top_holder_rssd_id=123456,
        )
        client = TestClient(app_fixture)
        lei_path = "testLeiPath"
        res = client.get(f"/v1/institutions/{lei_path}")
        assert res.status_code == 200
        assert res.json().get("name") == "Test Bank 123"

    def test_get_institution_not_exists(self, mocker: MockerFixture, app_fixture: FastAPI, authed_user_mock: Mock):
        get_institution_mock = mocker.patch(
            "regtech_user_fi_management.entities.repos.institutions_repo.get_institution"
        )
        get_institution_mock.return_value = None
        client = TestClient(app_fixture)
        lei_path = "testLeiPath"
        res = client.get(f"/v1/institutions/{lei_path}")
        get_institution_mock.assert_called_once_with(ANY, lei_path)
        assert res.status_code == 404

    def test_add_domains_unauthed(self, app_fixture: FastAPI, unauthed_user_mock: Mock):
        client = TestClient(app_fixture)

        lei_path = "testLeiPath"
        res = client.post(f"/v1/institutions/{lei_path}/domains/", json=[{"domain": "testDomain"}])
        assert res.status_code == 403

    def test_add_domains_authed(self, mocker: MockerFixture, app_fixture: FastAPI, authed_user_mock: Mock):
        add_domains_mock = mocker.patch("regtech_user_fi_management.entities.repos.institutions_repo.add_domains")
        add_domains_mock.return_value = [FinancialInstitutionDomainDao(domain="test.bank", lei="TESTBANK123000000000")]
        client = TestClient(app_fixture)

        lei_path = "testLeiPath"
        res = client.post(f"/v1/institutions/{lei_path}/domains/", json=[{"domain": "testDomain"}])
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
        lei_path = "testLeiPath"
        res = client.post(f"/v1/institutions/{lei_path}/domains/", json=[{"domain": "testDomain"}])
        assert res.status_code == 403

    def test_add_domains_authed_with_denied_email_domain(
        self, mocker: MockerFixture, app_fixture: FastAPI, authed_user_mock: Mock
    ):
        domain_denied_mock = mocker.patch("regtech_user_fi_management.dependencies.email_domain_denied")
        domain_denied_mock.return_value = True
        client = TestClient(app_fixture)
        lei_path = "testLeiPath"
        res = client.post(f"/v1/institutions/{lei_path}/domains/", json=[{"domain": "testDomain"}])
        assert res.status_code == 403
        assert "domain denied" in res.json()["error_detail"]

    def test_check_domain_allowed(self, mocker: MockerFixture, app_fixture: FastAPI, authed_user_mock: Mock):
        domain_allowed_mock = mocker.patch(
            "regtech_user_fi_management.entities.repos.institutions_repo.is_domain_allowed"
        )
        domain_allowed_mock.return_value = True
        domain_to_check = "local.host"
        client = TestClient(app_fixture)
        res = client.get(f"/v1/institutions/domains/allowed?domain={domain_to_check}")
        domain_allowed_mock.assert_called_once_with(ANY, domain_to_check)
        assert res.json() is True

    def test_get_associated_institutions(
        self, mocker: MockerFixture, app_fixture: FastAPI, auth_mock: Mock, get_institutions_mock: Mock
    ):
        get_institutions_mock.return_value = [
            FinancialInstitutionDao(
                name="Test Bank 123",
                lei="TESTBANK123000000000",
                is_active=True,
                domains=[FinancialInstitutionDomainDao(domain="test123.bank", lei="TESTBANK123000000000")],
                tax_id="12-3456789",
                rssd_id=1234,
                primary_federal_regulator_id="FRI1",
                primary_federal_regulator=FederalRegulatorDao(id="FRI1", name="FRI1"),
                hmda_institution_type_id="HIT1",
                hmda_institution_type=HMDAInstitutionTypeDao(id="HIT1", name="HIT1"),
                sbl_institution_types=[SblTypeMappingDao(sbl_type=SBLInstitutionTypeDao(id="SIT1", name="SIT1"))],
                hq_address_street_1="Test Address Street 1",
                hq_address_street_2="",
                hq_address_street_3="",
                hq_address_street_4="",
                hq_address_city="Test City 1",
                hq_address_state_code="GA",
                hq_address_state=AddressStateDao(code="GA", name="Georgia"),
                hq_address_zip="00000",
                parent_lei="012PARENTTESTBANK123",
                parent_legal_name="PARENT TEST BANK 123",
                parent_rssd_id=12345,
                top_holder_lei="01234TOPHOLDERLEI123",
                top_holder_legal_name="TOP HOLDER LEI 123",
                top_holder_rssd_id=123456,
            ),
            FinancialInstitutionDao(
                name="Test Bank 234",
                lei="TESTBANK234000000000",
                is_active=True,
                domains=[FinancialInstitutionDomainDao(domain="test234.bank", lei="TESTBANK234000000000")],
                tax_id="12-3456879",
                rssd_id=6879,
                primary_federal_regulator_id="FRI1",
                primary_federal_regulator=FederalRegulatorDao(id="FRI1", name="FRI1"),
                hmda_institution_type_id="HIT1",
                hmda_institution_type=HMDAInstitutionTypeDao(id="HIT1", name="HIT1"),
                sbl_institution_types=[SblTypeMappingDao(sbl_type=SBLInstitutionTypeDao(id="SIT1", name="SIT1"))],
                hq_address_street_1="Test Address Street 2",
                hq_address_street_2="",
                hq_address_street_3="",
                hq_address_street_4="",
                hq_address_city="Test City 2",
                hq_address_state_code="GA",
                hq_address_state=AddressStateDao(code="GA", name="Georgia"),
                hq_address_zip="00000",
                parent_lei="012PARENTTESTBANK123",
                parent_legal_name="PARENT TEST BANK 123",
                parent_rssd_id=14523,
                top_holder_lei="01234TOPHOLDERLEI123",
                top_holder_legal_name="TOP HOLDER LEI 123",
                top_holder_rssd_id=341256,
            ),
        ]
        claims = {
            "name": "test",
            "preferred_username": "test_user",
            "email": "test@test234.bank",
            "sub": "testuser123",
            "institutions": ["/TESTBANK123000000000", "/TESTBANK234000000000"],
        }
        auth_mock.return_value = (
            AuthCredentials(["authenticated"]),
            AuthenticatedUser.from_claim(claims),
        )
        client = TestClient(app_fixture)
        res = client.get("/v1/institutions/associated")
        assert res.status_code == 200
        get_institutions_mock.assert_called_once_with(ANY, ["TESTBANK123000000000", "TESTBANK234000000000"])
        data = res.json()
        inst1 = next(filter(lambda inst: inst["lei"] == "TESTBANK123000000000", data))
        inst2 = next(filter(lambda inst: inst["lei"] == "TESTBANK234000000000", data))
        assert inst1["approved"] is False
        assert inst2["approved"] is True

    def test_get_associated_institutions_with_no_institutions(
        self, app_fixture: FastAPI, auth_mock: Mock, get_institutions_mock: Mock
    ):
        get_institutions_mock.return_value = []
        claims = {
            "name": "test",
            "preferred_username": "test_user",
            "email": "test@test234.bank",
            "sub": "testuser123",
            "institutions": [],
        }
        auth_mock.return_value = (
            AuthCredentials(["authenticated"]),
            AuthenticatedUser.from_claim(claims),
        )
        client = TestClient(app_fixture)
        res = client.get("/v1/institutions/associated")
        assert res.status_code == 200
        get_institutions_mock.assert_called_once_with(ANY, [])
        assert res.json() == []

    def test_get_institution_types(self, mocker: MockerFixture, app_fixture: FastAPI, authed_user_mock: Mock):
        mock = mocker.patch("regtech_user_fi_management.entities.repos.institutions_repo.get_sbl_types")
        mock.return_value = []
        client = TestClient(app_fixture)
        res = client.get("/v1/institutions/types/sbl")
        assert res.status_code == 200

        mock = mocker.patch("regtech_user_fi_management.entities.repos.institutions_repo.get_hmda_types")
        mock.return_value = []
        res = client.get("/v1/institutions/types/hmda")
        assert res.status_code == 200

        res = client.get("/v1/institutions/types/blah")
        assert res.status_code == 422

    def test_get_address_states(self, mocker: MockerFixture, app_fixture: FastAPI, authed_user_mock: Mock):
        mock = mocker.patch("regtech_user_fi_management.entities.repos.institutions_repo.get_address_states")
        mock.return_value = []
        client = TestClient(app_fixture)
        res = client.get("/v1/institutions/address-states")
        assert res.status_code == 200

    def test_get_federal_regulators(self, mocker: MockerFixture, app_fixture: FastAPI, authed_user_mock: Mock):
        mock = mocker.patch("regtech_user_fi_management.entities.repos.institutions_repo.get_federal_regulators")
        mock.return_value = []
        client = TestClient(app_fixture)
        res = client.get("/v1/institutions/regulators")
        assert res.status_code == 200

    def test_get_sbl_types(self, mocker: MockerFixture, app_fixture: FastAPI, authed_user_mock: Mock):
        inst_version = 2
        get_institution_mock = mocker.patch(
            "regtech_user_fi_management.entities.repos.institutions_repo.get_institution"
        )
        get_institution_mock.return_value = FinancialInstitutionDao(
            version=inst_version,
            name="Test Bank 123",
            lei="TESTBANK123000000000",
            is_active=True,
            domains=[FinancialInstitutionDomainDao(domain="test.bank", lei="TESTBANK123000000000")],
            tax_id="12-3456789",
            rssd_id=1234,
            primary_federal_regulator_id="FRI1",
            primary_federal_regulator=FederalRegulatorDao(id="FRI1", name="FRI1"),
            hmda_institution_type_id="HIT1",
            hmda_institution_type=HMDAInstitutionTypeDao(id="HIT1", name="HIT1"),
            sbl_institution_types=[SblTypeMappingDao(sbl_type=SBLInstitutionTypeDao(id="SIT1", name="SIT1"))],
            hq_address_street_1="Test Address Street 1",
            hq_address_street_2="",
            hq_address_street_3="",
            hq_address_street_4="",
            hq_address_city="Test City 1",
            hq_address_state_code="GA",
            hq_address_state=AddressStateDao(code="GA", name="Georgia"),
            hq_address_zip="00000",
            parent_lei="012PARENTTESTBANK123",
            parent_legal_name="PARENT TEST BANK 123",
            parent_rssd_id=12345,
            top_holder_lei="01234TOPHOLDERLEI123",
            top_holder_legal_name="TOP HOLDER LEI 123",
            top_holder_rssd_id=123456,
        )
        client = TestClient(app_fixture)
        test_lei = "TESTBANK123000000000"
        res = client.get(f"/v1/institutions/{test_lei}/types/sbl")
        assert res.status_code == HTTPStatus.OK
        result = res.json()
        assert len(result["data"]) == 1
        assert result["version"] == inst_version
        assert result["data"][0] == {"sbl_type": {"id": "SIT1", "name": "SIT1"}, "details": None}

    def test_get_sbl_types_no_institution(self, mocker: MockerFixture, app_fixture: FastAPI, authed_user_mock: Mock):
        get_institution_mock = mocker.patch(
            "regtech_user_fi_management.entities.repos.institutions_repo.get_institution"
        )
        get_institution_mock.return_value = None
        client = TestClient(app_fixture)
        test_lei = "TESTBANK123000000000"
        res = client.get(f"/v1/institutions/{test_lei}/types/sbl")
        assert res.status_code == HTTPStatus.NO_CONTENT

    def test_get_hmda_types(self, mocker: MockerFixture, app_fixture: FastAPI, authed_user_mock: Mock):
        client = TestClient(app_fixture)
        test_lei = "TESTBANK123000000000"
        res = client.get(f"/v1/institutions/{test_lei}/types/hmda")
        assert res.status_code == HTTPStatus.NOT_IMPLEMENTED

    def test_update_institution_types(self, mocker: MockerFixture, app_fixture: FastAPI, authed_user_mock: Mock):
        mock = mocker.patch("regtech_user_fi_management.entities.repos.institutions_repo.update_sbl_types")
        client = TestClient(app_fixture)
        test_lei = "TESTBANK123000000000"
        res = client.put(
            f"/v1/institutions/{test_lei}/types/sbl",
            json={"sbl_institution_types": ["1", {"id": "2"}, {"id": "13", "details": "test"}]},
        )
        assert res.status_code == HTTPStatus.OK
        mock.assert_called_once_with(
            ANY, ANY, test_lei, ["1", SblTypeAssociationDto(id="2"), SblTypeAssociationDto(id="13", details="test")]
        )

    def test_update_non_existing_institution_types(
        self, mocker: MockerFixture, app_fixture: FastAPI, authed_user_mock: Mock
    ):
        get_institution_mock = mocker.patch(
            "regtech_user_fi_management.entities.repos.institutions_repo.get_institution"
        )
        get_institution_mock.return_value = None
        client = TestClient(app_fixture)
        test_lei = "TESTBANK123000000000"
        res = client.put(
            f"/v1/institutions/{test_lei}/types/sbl",
            json={"sbl_institution_types": ["1", {"id": "2"}, {"id": "13", "details": "test"}]},
        )
        assert res.status_code == HTTPStatus.NO_CONTENT

    def test_update_unsupported_institution_types(
        self, mocker: MockerFixture, app_fixture: FastAPI, authed_user_mock: Mock
    ):
        mock = mocker.patch("regtech_user_fi_management.entities.repos.institutions_repo.update_sbl_types")
        client = TestClient(app_fixture)
        test_lei = "TESTBANK123000000000"
        res = client.put(
            f"/v1/institutions/{test_lei}/types/hmda",
            json={"sbl_institution_types": ["1", {"id": "2"}, {"id": "13", "details": "test"}]},
        )
        assert res.status_code == HTTPStatus.NOT_IMPLEMENTED
        mock.assert_not_called()

    def test_update_wrong_institution_types(self, mocker: MockerFixture, app_fixture: FastAPI, authed_user_mock: Mock):
        mock = mocker.patch("regtech_user_fi_management.entities.repos.institutions_repo.update_sbl_types")
        client = TestClient(app_fixture)
        test_lei = "TESTBANK123000000000"
        res = client.put(
            f"/v1/institutions/{test_lei}/types/test",
            json={"sbl_institution_types": ["1", {"id": "2"}, {"id": "13", "details": "test"}]},
        )
        assert res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        mock.assert_not_called()
