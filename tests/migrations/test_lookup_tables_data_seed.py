from sqlalchemy import text
from sqlalchemy.engine import Engine
from pytest_alembic import MigrationContext


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
    sbl_institution_type_expected = [("1", "Bank or savings association.")]

    assert sbl_institution_type_rows == sbl_institution_type_expected
