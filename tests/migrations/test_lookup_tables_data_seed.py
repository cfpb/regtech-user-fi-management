import pytest
from sqlalchemy import text
from sqlalchemy.engine import Engine
from pytest_alembic import MigrationContext


@pytest.fixture
def alembic_config():
    return {
        "at_revision_data": {
            "7b6ff51002b5": {"__tablename__": "address_state", "code": "ZZ", "name": "TestState"},
            "26a742d97ad9": {"__tablename__": "federal_regulator", "id": "ZZZ", "name": "TestRegulator"},
            "f4ff7d1aa6df": {"__tablename__": "hmda_institution_type", "id": "00", "name": "TestHmdaInstitutionType"},
            "a41281b1e109": {"__tablename__": "sbl_institution_type", "id": "00", "name": "TestSblInstitutionType"},
        }
    }


def test_address_state_data_seed(alembic_runner: MigrationContext, alembic_engine: Engine):
    # Migrate up to, but not including this new migration
    alembic_runner.migrate_up_before("7b6ff51002b5")

    # Test address_state seed
    address_state_tablename = "address_state"
    alembic_runner.migrate_up_one()
    with alembic_engine.connect() as conn:
        address_state_rows = conn.execute(
            text("SELECT code, name from %s where code = :code" % address_state_tablename), (dict(code="AL"))
        ).fetchall()
    address_state_expected = [("AL", "Alabama")]
    assert address_state_rows == address_state_expected

    alembic_runner.migrate_down_one()
    with alembic_engine.connect() as conn:
        address_state_before_seed = conn.execute(text("SELECT code, name FROM %s" % address_state_tablename)).fetchall()
    assert address_state_before_seed == [("ZZ", "TestState")]


def test_federal_regulator_data_seed(alembic_runner: MigrationContext, alembic_engine: Engine):
    # Migrate up to, but not including this new migration
    alembic_runner.migrate_up_before("26a742d97ad9")

    # Test federal_regulator seed
    federal_regulator_tablename = "federal_regulator"
    alembic_runner.migrate_up_one()
    with alembic_engine.connect() as conn:
        federal_regulator_rows = conn.execute(
            text("SELECT id, name from %s where id = :id" % federal_regulator_tablename), (dict(id="FCA"))
        ).fetchall()
    federal_regulator_expected = [
        ("FCA", "Farm Credit Administration"),
    ]

    assert federal_regulator_rows == federal_regulator_expected

    alembic_runner.migrate_down_one()
    with alembic_engine.connect() as conn:
        federal_regulator_before_seed = conn.execute(
            text("SELECT id, name FROM %s" % federal_regulator_tablename)
        ).fetchall()
    assert federal_regulator_before_seed == [("ZZZ", "TestRegulator")]


def test_hmda_institution_type_data_seed(alembic_runner: MigrationContext, alembic_engine: Engine):
    # Migrate up to, but not including this new migration
    alembic_runner.migrate_up_before("f4ff7d1aa6df")

    # Test hmda_institution_type seed
    hmda_institution_type_tablename = "hmda_institution_type"
    alembic_runner.migrate_up_one()
    with alembic_engine.connect() as conn:
        hmda_institution_type_rows = conn.execute(
            # text("SELECT id, name from %s" % hmda_institution_type_tablename)
            text("SELECT id, name from %s where id = :id" % hmda_institution_type_tablename),
            (dict(id="1")),
        ).fetchall()
    hmda_institution_type_expected = [("1", "National Bank (OCC supervised)")]

    assert hmda_institution_type_rows == hmda_institution_type_expected

    alembic_runner.migrate_down_one()
    with alembic_engine.connect() as conn:
        hmda_institution_type_before_seed = conn.execute(
            text("SELECT id, name FROM %s" % hmda_institution_type_tablename)
        ).fetchall()
    assert hmda_institution_type_before_seed == [("00", "TestHmdaInstitutionType")]


def test_sbl_institution_type_data_seed(alembic_runner: MigrationContext, alembic_engine: Engine):
    # Migrate up to, but not including this new migration
    alembic_runner.migrate_up_before("a41281b1e109")

    # Test sbl_institution_type seed
    sbl_institution_type_tablename = "sbl_institution_type"
    alembic_runner.migrate_up_one()
    with alembic_engine.connect() as conn:
        sbl_institution_type_rows = conn.execute(
            text("SELECT id, name from %s where id = :id " % sbl_institution_type_tablename), (dict(id="1"))
        ).fetchall()
    sbl_institution_type_expected = [("1", "Bank or savings association")]

    assert sbl_institution_type_rows == sbl_institution_type_expected

    alembic_runner.migrate_down_one()
    with alembic_engine.connect() as conn:
        sbl_institution_type_before_seed = conn.execute(
            text("SELECT id, name FROM %s" % sbl_institution_type_tablename)
        ).fetchall()
    assert sbl_institution_type_before_seed == [("00", "TestSblInstitutionType")]
