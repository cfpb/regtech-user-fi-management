import pytest

from pytest_mock import MockerFixture


@pytest.fixture(autouse=True)
def setup(mocker: MockerFixture):
    mocked_engine = mocker.patch("sqlalchemy.ext.asyncio.create_async_engine")
    MockedEngine = mocker.patch("sqlalchemy.ext.asyncio.AsyncEngine")
    mocked_engine.return_value = MockedEngine.return_value
    mocker.patch("fastapi.security.OAuth2AuthorizationCodeBearer")
    mocker.patch("entities.engine.get_session")
