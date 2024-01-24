from unittest.mock import Mock

import pytest
from fastapi import FastAPI
from pytest_mock import MockerFixture
from starlette.authentication import AuthCredentials, UnauthenticatedUser
from regtech_api_commons.models.auth import AuthenticatedUser
from entities.models import (
    FinancialInstitutionDao,
    FinancialInstitutionDomainDao,
    FederalRegulatorDao,
    AddressStateDao,
    HMDAInstitutionTypeDao,
    SBLInstitutionTypeDao,
    SblTypeMappingDao,
)


@pytest.fixture
def app_fixture(mocker: MockerFixture) -> FastAPI:
    mocked_engine = mocker.patch("sqlalchemy.ext.asyncio.create_async_engine")
    MockedEngine = mocker.patch("sqlalchemy.ext.asyncio.AsyncEngine")
    mocked_engine.return_value = MockedEngine.return_value
    mocker.patch("fastapi.security.OAuth2AuthorizationCodeBearer")
    domain_denied_mock = mocker.patch("dependencies.email_domain_denied")
    domain_denied_mock.return_value = False
    from main import app

    return app


@pytest.fixture
def auth_mock(mocker: MockerFixture) -> Mock:
    return mocker.patch("regtech_api_commons.oauth2.oauth2_backend.BearerTokenAuthBackend.authenticate")


@pytest.fixture
def authed_user_mock(auth_mock: Mock) -> Mock:
    claims = {
        "name": "test",
        "preferred_username": "test_user",
        "email": "test@local.host",
        "sub": "testuser123",
    }
    auth_mock.return_value = (
        AuthCredentials(["manage-account", "query-groups", "manage-users", "authenticated"]),
        AuthenticatedUser.from_claim(claims),
    )
    return auth_mock


@pytest.fixture
def unauthed_user_mock(auth_mock: Mock) -> Mock:
    auth_mock.return_value = (AuthCredentials("unauthenticated"), UnauthenticatedUser())
    return auth_mock


@pytest.fixture
def get_institutions_mock(mocker: MockerFixture) -> Mock:
    mock = mocker.patch("entities.repos.institutions_repo.get_institutions")
    mock.return_value = [
        FinancialInstitutionDao(
            name="Test Bank 123",
            lei="TESTBANK123",
            is_active=True,
            domains=[FinancialInstitutionDomainDao(domain="test.bank", lei="TESTBANK123")],
            tax_id="123456789",
            rssd_id=1234,
            primary_federal_regulator_id="FRI1",
            primary_federal_regulator=FederalRegulatorDao(id="FRI1", name="FRI1"),
            hmda_institution_type_id="HIT1",
            hmda_institution_type=HMDAInstitutionTypeDao(id="HIT1", name="HIT1"),
            sbl_institution_types=[SblTypeMappingDao(sbl_type=SBLInstitutionTypeDao(id="SIT1", name="SIT1"))],
            hq_address_street_1="Test Address Street 1",
            hq_address_street_2="",
            hq_address_city="Test City 1",
            hq_address_state_code="GA",
            hq_address_state=AddressStateDao(code="GA", name="Georgia"),
            hq_address_zip="00000",
            parent_lei="PARENTTESTBANK123",
            parent_legal_name="PARENT TEST BANK 123",
            parent_rssd_id=12345,
            top_holder_lei="TOPHOLDERLEI123",
            top_holder_legal_name="TOP HOLDER LEI 123",
            top_holder_rssd_id=123456,
        )
    ]
    return mock
