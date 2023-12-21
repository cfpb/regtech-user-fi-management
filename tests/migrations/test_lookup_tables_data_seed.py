from sqlalchemy import text
from sqlalchemy.engine import Engine
from pytest_alembic import MigrationContext

from seed import (
    address_state_seed,
    federal_regulator_seed,
    hmda_institution_type_seed,
    sbl_institution_type_seed,
)


def test_address_state_data_seed(alembic_runner: MigrationContext, alembic_engine: Engine):
    # Migrate up to, but not including this new migration
    alembic_runner.migrate_up_before("7b6ff51002b5")

    # Test address_state feed
    address_state_tablename = "address_state"
    alembic_runner.migrate_up_one()
    with alembic_engine.connect() as conn:
        address_state_rows = conn.execute(text("SELECT code, name from %s" % address_state_tablename)).fetchall()
    address_state_expected = [tuple(dict.values()) for dict in address_state_seed]

    assert address_state_rows == address_state_expected


def test_federal_regulator_data_seed(alembic_runner: MigrationContext, alembic_engine: Engine):
    # Migrate up to, but not including this new migration
    alembic_runner.migrate_up_before("26a742d97ad9")

    # Test federal_regulator feed
    federal_regulator_tablename = "federal_regulator"
    alembic_runner.migrate_up_one()
    with alembic_engine.connect() as conn:
        federal_regulator_rows = conn.execute(text("SELECT id, name from %s" % federal_regulator_tablename)).fetchall()
    federal_regulator_expected = [tuple(dict.values()) for dict in federal_regulator_seed]

    assert federal_regulator_rows == federal_regulator_expected


def test_hmda_institution_type_data_seed(alembic_runner: MigrationContext, alembic_engine: Engine):
    # Migrate up to, but not including this new migration
    alembic_runner.migrate_up_before("f4ff7d1aa6df")

    # Test hmda_institution_type feed
    hmda_institution_type_tablename = "hmda_institution_type"
    alembic_runner.migrate_up_one()
    with alembic_engine.connect() as conn:
        hmda_institution_type_rows = conn.execute(
            text("SELECT id, name from %s" % hmda_institution_type_tablename)
        ).fetchall()
    hmda_institution_type_expected = [tuple(dict.values()) for dict in hmda_institution_type_seed]

    assert hmda_institution_type_rows == hmda_institution_type_expected


def test_sbl_institution_type_data_seed(alembic_runner: MigrationContext, alembic_engine: Engine):
    # Migrate up to, but not including this new migration
    alembic_runner.migrate_up_before("a41281b1e109")

    # Test sbl_institution_type feed
    sbl_institution_type_tablename = "sbl_institution_type"
    alembic_runner.migrate_up_one()
    with alembic_engine.connect() as conn:
        sbl_institution_type_rows = conn.execute(
            text("SELECT id, name from %s" % sbl_institution_type_tablename)
        ).fetchall()
    sbl_institution_type_expected = [tuple(dict.values()) for dict in sbl_institution_type_seed]

    assert sbl_institution_type_rows == sbl_institution_type_expected
