from pytest_mock import MockerFixture
from sqlalchemy.ext.asyncio import AsyncSession

import pytest


@pytest.fixture
def mock_session(mocker: MockerFixture) -> AsyncSession:
    return mocker.patch("sqlalchemy.ext.asyncio.AsyncSession").return_value


async def test_domain_denied(mocker: MockerFixture, mock_session: AsyncSession):
    domain_allowed_mock = mocker.patch("regtech_user_fi_management.entities.repos.institutions_repo.is_domain_allowed")
    domain_allowed_mock.return_value = False
    from regtech_user_fi_management.dependencies import email_domain_denied

    denied_domain = "denied.domain"

    assert await email_domain_denied(mock_session, denied_domain) is True
    domain_allowed_mock.assert_called_once_with(mock_session, denied_domain)


async def test_domain_allowed(mocker: MockerFixture, mock_session: AsyncSession):
    domain_allowed_mock = mocker.patch("regtech_user_fi_management.entities.repos.institutions_repo.is_domain_allowed")
    domain_allowed_mock.return_value = True
    from regtech_user_fi_management.dependencies import email_domain_denied

    allowed_domain = "allowed.domain"

    assert await email_domain_denied(mock_session, allowed_domain) is False
    domain_allowed_mock.assert_called_once_with(mock_session, allowed_domain)
