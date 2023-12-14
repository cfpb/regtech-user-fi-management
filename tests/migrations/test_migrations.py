from pytest_alembic.tests import (
    test_single_head_revision,  # noqa: F401
    test_up_down_consistency,  # noqa: F401
    test_upgrade,  # noqa: F401
)

import sqlalchemy
from sqlalchemy import text
from sqlalchemy.engine import Engine

from pytest_alembic import MigrationContext


def test_tables_exist_after_migration(alembic_runner: MigrationContext, alembic_engine: Engine):
    alembic_runner.migrate_up_to("045aa502e050")

    inspector = sqlalchemy.inspect(alembic_engine)
    tables = inspector.get_table_names()
    assert "denied_domains" in tables
    assert "financial_institutions" in tables
    assert "financial_institution_domains" in tables
    assert "address_state" in tables
    assert "federal_regulator" in tables
    assert "hmda_institution_type" in tables
    assert "sbl_institution_type" in tables


def test_data_feed_after_migration_045aa502e050(alembic_runner: MigrationContext, alembic_engine: Engine):
    # Migrate up to, but not including this new migration
    alembic_runner.migrate_up_before("045aa502e050")

    # Test address_state feed
    alembic_runner.insert_into("address_state", dict(code="TS", name="Test State"))
    alembic_runner.migrate_up_one()
    with alembic_engine.connect() as conn:
        address_state_rows = conn.execute(text("SELECT code from address_state")).fetchall()
    assert address_state_rows == [("TS",)]

    # Test federal_regulator feed
    alembic_runner.insert_into("federal_regulator", dict(id="TFCA", name="Test Farm Credit Administration"))
    alembic_runner.migrate_up_one()
    with alembic_engine.connect() as conn:
        address_state_rows = conn.execute(text("SELECT id from federal_regulator")).fetchall()
    assert address_state_rows == [("TFCA",)]

    # Test hmda_institution_type feed
    alembic_runner.insert_into(
        "hmda_institution_type", dict(id="T8", name="Test Branch or Agency of FBO (FRS supervised)")
    )
    alembic_runner.migrate_up_one()
    with alembic_engine.connect() as conn:
        address_state_rows = conn.execute(text("SELECT id from hmda_institution_type")).fetchall()
    assert address_state_rows == [("T8",)]

    # Test sbl_institution_type feed
    alembic_runner.insert_into("sbl_institution_type", dict(id="T12", name="Test Online lender"))
    alembic_runner.migrate_up_one()
    with alembic_engine.connect() as conn:
        address_state_rows = conn.execute(text("SELECT id from sbl_institution_type")).fetchall()
    assert address_state_rows == [("T12",)]
