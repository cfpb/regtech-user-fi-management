import pytest

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import scoped_session, sessionmaker
from regtech_user_fi_management.entities.models.dao import Base


@pytest.fixture(scope="session")
def engine():
    return create_engine("sqlite://")


@pytest.fixture(scope="function", autouse=True)
def setup_db(
    request: pytest.FixtureRequest,
    engine: Engine,
):

    Base.metadata.create_all(bind=engine)

    def teardown():
        Base.metadata.drop_all(bind=engine)

    request.addfinalizer(teardown)


@pytest.fixture(scope="function")
def transaction_session(session_generator: scoped_session):
    with session_generator() as session:
        yield session


@pytest.fixture(scope="function")
def query_session(session_generator: scoped_session):
    with session_generator() as session:
        yield session


@pytest.fixture(scope="function")
def session_generator(engine: Engine):
    return scoped_session(sessionmaker(engine, expire_on_commit=False))
