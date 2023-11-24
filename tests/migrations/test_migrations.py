from pytest_alembic.tests import (
    test_single_head_revision,  # noqa: F401
    test_up_down_consistency,  # noqa: F401
    test_upgrade,  # noqa: F401
)

import sqlalchemy
from sqlalchemy.engine import Engine

from pytest_alembic import MigrationContext


def test_tables_exist_after_migration(alembic_runner: MigrationContext, alembic_engine: Engine):
    alembic_runner.migrate_up_to("20e0d51d8be9")

    inspector = sqlalchemy.inspect(alembic_engine)
    tables = inspector.get_table_names()
    assert "denied_domains" in tables
    assert "financial_institutions" in tables
    assert "financial_institution_domains" in tables
