from unittest.mock import Mock

import pytest
from fastapi import FastAPI
from pytest_mock import MockerFixture
from starlette.authentication import AuthCredentials, UnauthenticatedUser

from oauth2.oauth2_backend import AuthenticatedUser


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
    return mocker.patch("oauth2.oauth2_backend.BearerTokenAuthBackend.authenticate")


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
