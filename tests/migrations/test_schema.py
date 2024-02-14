import sqlalchemy
from sqlalchemy.engine import Engine

from pytest_alembic import MigrationContext


def test_financial_institutions_schema_migrate_up_to_045aa502e050(
    alembic_runner: MigrationContext, alembic_engine: Engine
):
    alembic_runner.migrate_up_to("045aa502e050")

    inspector = sqlalchemy.inspect(alembic_engine)
    expected_columns = [
        "lei",
        "name",
        "event_time",
        "tax_id",
        "rssd_id",
        "primary_federal_regulator_id",
        "hmda_institution_type_id",
        "sbl_institution_type_id",
        "hq_address_street_1",
        "hq_address_street_2",
        "hq_address_city",
        "hq_address_state_code",
        "hq_address_zip",
        "parent_lei",
        "parent_legal_name",
        "parent_rssd_id",
        "top_holder_lei",
        "top_holder_legal_name",
        "top_holder_rssd_id",
    ]

    columns = inspector.get_columns("financial_institutions")
    columns_names = [column.get("name") for column in columns]

    assert columns_names == expected_columns


def test_financial_institutions_schema_migrate_up_to_20e0d51d8be9(
    alembic_runner: MigrationContext, alembic_engine: Engine
):
    alembic_runner.migrate_up_to("20e0d51d8be9")

    inspector = sqlalchemy.inspect(alembic_engine)
    expected_columns = [
        "lei",
        "name",
        "event_time",
    ]

    columns = inspector.get_columns("financial_institutions")
    columns_names = [column.get("name") for column in columns]

    assert columns_names == expected_columns


def test_fi_types_table_6826f05140cd(alembic_runner: MigrationContext, alembic_engine: Engine):
    alembic_runner.migrate_up_to("6826f05140cd")
    inspector = sqlalchemy.inspect(alembic_engine)
    expected_columns = ["fi_id", "type_id", "details"]
    columns = inspector.get_columns("fi_to_type_mapping")
    columns_names = [column.get("name") for column in columns]

    assert columns_names == expected_columns


def test_fi_versioning_tables_3f893e52d05c(alembic_runner: MigrationContext, alembic_engine: Engine):
    alembic_runner.migrate_up_to("3f893e52d05c")
    inspector = sqlalchemy.inspect(alembic_engine)
    fi_columns = inspector.get_columns("financial_institutions")
    assert "version" in [column.get("name") for column in fi_columns]
    mapping_columns = inspector.get_columns("fi_to_type_mapping")
    assert "version" in [column.get("name") for column in mapping_columns]


def test_fi_history_table_columns_8106d83ff594(alembic_runner: MigrationContext, alembic_engine: Engine):
    alembic_runner.migrate_up_to("8106d83ff594")
    inspector = sqlalchemy.inspect(alembic_engine)
    fi_columns = inspector.get_columns("financial_institutions")
    mapping_columns = inspector.get_columns("fi_to_type_mapping")
    fi_history_columns = inspector.get_columns("financial_institutions_history")
    mapping_history_columns = inspector.get_columns("fi_to_type_mapping_history")
    assert {column.get("name") for column in fi_columns}.issubset({column.get("name") for column in fi_history_columns})
    assert {column.get("name") for column in mapping_columns}.issubset(
        {column.get("name") for column in mapping_history_columns}
    )
