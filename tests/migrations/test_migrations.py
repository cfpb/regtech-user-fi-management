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


def test_fi_history_tables_0e520c01fb42(alembic_runner: MigrationContext, alembic_engine: Engine):
    alembic_runner.migrate_up_to("0e520c01fb42")
    inspector = sqlalchemy.inspect(alembic_engine)

    tax_column = [c for c in inspector.get_columns("financial_institutions") if c["name"] == "tax_id"][0]
    assert tax_column["type"].length == 10

    tax_column = [c for c in inspector.get_columns("financial_institutions_history") if c["name"] == "tax_id"][0]
    assert tax_column["type"].length == 10


def test_migration_to_2ad66aaf4583(alembic_runner: MigrationContext, alembic_engine: Engine):
    alembic_runner.migrate_up_to("2ad66aaf4583")

    inspector = sqlalchemy.inspect(alembic_engine)

    assert "hq_address_street_3" in [c["name"] for c in inspector.get_columns("financial_institutions")]
    assert "hq_address_street_4" in [c["name"] for c in inspector.get_columns("financial_institutions")]


def test_migration_to_6dd77f09fae6(alembic_runner: MigrationContext, alembic_engine: Engine):

    alembic_runner.migrate_up_to("6dd77f09fae6")

    inspector = sqlalchemy.inspect(alembic_engine)

    columns = inspector.get_columns("financial_institutions")

    assert [c for c in columns if c["name"] == "name"][0]["type"].length is None
    assert [c for c in columns if c["name"] == "hq_address_street_1"][0]["type"].length is None
    assert [c for c in columns if c["name"] == "hq_address_street_2"][0]["type"].length is None
    assert [c for c in columns if c["name"] == "hq_address_street_3"][0]["type"].length is None
    assert [c for c in columns if c["name"] == "hq_address_street_4"][0]["type"].length is None
    assert [c for c in columns if c["name"] == "hq_address_city"][0]["type"].length is None
    assert [c for c in columns if c["name"] == "parent_legal_name"][0]["type"].length is None
    assert [c for c in columns if c["name"] == "top_holder_legal_name"][0]["type"].length is None


def test_tables_exist_migrate_up_to_6613e1e2c133(alembic_runner: MigrationContext, alembic_engine: Engine):
    alembic_runner.migrate_up_to("6613e1e2c133")

    inspector = sqlalchemy.inspect(alembic_engine)
    tables = inspector.get_table_names()
    assert "lei_status" in tables


def test_migration_to_ca39ad68af05(alembic_runner: MigrationContext, alembic_engine: Engine):

    alembic_runner.migrate_up_to("ca39ad68af05")

    inspector = sqlalchemy.inspect(alembic_engine)

    columns = inspector.get_columns("financial_institutions")

    assert [c for c in columns if c["name"] == "name"][0]["type"].length is None
    assert [c for c in columns if c["name"] == "hq_address_street_1"][0]["type"].length is None
    assert [c for c in columns if c["name"] == "hq_address_street_2"][0]["type"].length is None
    assert [c for c in columns if c["name"] == "hq_address_street_3"][0]["type"].length is None
    assert [c for c in columns if c["name"] == "hq_address_street_4"][0]["type"].length is None
    assert [c for c in columns if c["name"] == "hq_address_city"][0]["type"].length is None
    assert [c for c in columns if c["name"] == "parent_legal_name"][0]["type"].length is None
    assert [c for c in columns if c["name"] == "top_holder_legal_name"][0]["type"].length is None
