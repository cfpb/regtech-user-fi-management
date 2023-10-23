import pytest

from pytest_alembic.config import Config
from sqlalchemy.ext.asyncio import create_async_engine


@pytest.fixture
def alembic_config():
    """Override this fixture to configure the exact alembic context setup required."""
    return Config()


@pytest.fixture
def alembic_engine():
    """Override this fixture to provide pytest-alembic powered tests with a database handle."""
    return create_async_engine("sqlite+aiosqlite://")
