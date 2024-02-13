from pytest_alembic.tests import (
    test_single_head_revision,  # noqa: F401
    test_up_down_consistency,  # noqa: F401
    test_upgrade,  # noqa: F401
)

import sqlalchemy
from sqlalchemy.engine import Engine

from pytest_alembic import MigrationContext


def test_tables_exist_migrate_up_to_045aa502e050(alembic_runner: MigrationContext, alembic_engine: Engine):
    alembic_runner.migrate_up_to("045aa502e050")

    inspector = sqlalchemy.inspect(alembic_engine)
    tables = inspector.get_table_names()
    assert "address_state" in tables
    assert "federal_regulator" in tables
    assert "hmda_institution_type" in tables
    assert "sbl_institution_type" in tables


def test_tables_exist_migrate_up_to_20e0d51d8be9(alembic_runner: MigrationContext, alembic_engine: Engine):
    alembic_runner.migrate_up_to("20e0d51d8be9")

    inspector = sqlalchemy.inspect(alembic_engine)
    tables = inspector.get_table_names()
    assert "denied_domains" in tables
    assert "financial_institutions" in tables
    assert "financial_institution_domains" in tables


def test_tables_not_exist_migrate_down_to_base(alembic_runner: MigrationContext, alembic_engine: Engine):
    alembic_runner.migrate_down_to("base")

    inspector = sqlalchemy.inspect(alembic_engine)
    tables = inspector.get_table_names()
    assert "denied_domains" not in tables
    assert "financial_institutions" not in tables
    assert "financial_institution_domains" not in tables


def test_fi_history_tables_8106d83ff594(alembic_runner: MigrationContext, alembic_engine: Engine):
    alembic_runner.migrate_up_to("8106d83ff594")
    inspector = sqlalchemy.inspect(alembic_engine)
    tables = inspector.get_table_names()
    assert "financial_institutions_history" in tables
    assert "fi_to_type_mapping_history" in tables
