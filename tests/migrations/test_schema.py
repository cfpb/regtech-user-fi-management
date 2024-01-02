import sqlalchemy
from sqlalchemy.engine import Engine

from pytest_alembic import MigrationContext


def test_financial_institutions_schema_migrate_up_to_045aa502e050(
    alembic_runner: MigrationContext, alembic_engine: Engine
):
    alembic_runner.migrate_up_to("045aa502e050")

    inspector = sqlalchemy.inspect(alembic_engine)
    expexted_columns = [
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

    assert columns_names == expexted_columns


def test_financial_institutions_schema_migrate_up_to_20e0d51d8be9(
    alembic_runner: MigrationContext, alembic_engine: Engine
):
    alembic_runner.migrate_up_to("20e0d51d8be9")

    inspector = sqlalchemy.inspect(alembic_engine)
    expexted_columns = [
        "lei",
        "name",
        "event_time",
    ]

    columns = inspector.get_columns("financial_institutions")
    columns_names = [column.get("name") for column in columns]

    assert columns_names == expexted_columns