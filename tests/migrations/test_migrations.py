from pytest_alembic.tests import (
    test_single_head_revision,  # noqa: F401
    test_up_down_consistency,  # noqa: F401
    test_upgrade,  # noqa: F401
)

import sqlalchemy
from sqlalchemy import text
from sqlalchemy.engine import Engine
import os
import csv
from entities.models import AddressStateDao, FederalRegulatorDao, HMDAInstitutionTypeDao, SBLInstitutionTypeDao

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


def data_feed_migration_helper(table_name):
    file_dir = os.path.dirname(os.path.realpath(__file__))
    data_file_path = f"{file_dir}/../../db_revisions/feed/%s.csv" % table_name
    with open(data_file_path) as f:
        reader = csv.reader(f, delimiter="|")
        next(reader)
        output_list = list(tuple(line) for line in reader)
    return output_list


def test_address_state_data_feed(alembic_runner: MigrationContext, alembic_engine: Engine):
    # Migrate up to, but not including this new migration
    alembic_runner.migrate_up_before("7b6ff51002b5")

    # Test address_state feed
    address_state_tablename = AddressStateDao.__tablename__
    alembic_runner.migrate_up_one()
    with alembic_engine.connect() as conn:
        address_state_rows = conn.execute(text("SELECT code, name from %s" % address_state_tablename)).fetchall()
    address_state_expected = data_feed_migration_helper(address_state_tablename)
    assert address_state_rows == address_state_expected


def test_federal_regulator_data_feed(alembic_runner: MigrationContext, alembic_engine: Engine):
    # Migrate up to, but not including this new migration
    alembic_runner.migrate_up_before("26a742d97ad9")

    # Test federal_regulator feed
    federal_regulator_tablename = FederalRegulatorDao.__tablename__
    alembic_runner.migrate_up_one()
    with alembic_engine.connect() as conn:
        federal_regulator_rows = conn.execute(text("SELECT id, name from %s" % federal_regulator_tablename)).fetchall()
    federal_regulator_expected = data_feed_migration_helper(federal_regulator_tablename)
    assert federal_regulator_rows == federal_regulator_expected


def test_hmda_institution_type_data_feed(alembic_runner: MigrationContext, alembic_engine: Engine):
    # Migrate up to, but not including this new migration
    alembic_runner.migrate_up_before("f4ff7d1aa6df")

    # Test hmda_institution_type feed
    hmda_institution_type_tablename = HMDAInstitutionTypeDao.__tablename__
    alembic_runner.migrate_up_one()
    with alembic_engine.connect() as conn:
        hmda_institution_type_rows = conn.execute(
            text("SELECT id, name from %s" % hmda_institution_type_tablename)
        ).fetchall()
    hmda_institution_type_expected = data_feed_migration_helper(hmda_institution_type_tablename)
    assert hmda_institution_type_rows == hmda_institution_type_expected


def test_sbl_institution_type_data_feed(alembic_runner: MigrationContext, alembic_engine: Engine):
    # Migrate up to, but not including this new migration
    alembic_runner.migrate_up_before("a41281b1e109")

    # Test sbl_institution_type feed
    sbl_institution_type_tablename = SBLInstitutionTypeDao.__tablename__
    alembic_runner.migrate_up_one()
    with alembic_engine.connect() as conn:
        sbl_institution_type_rows = conn.execute(
            text("SELECT id, name from %s" % sbl_institution_type_tablename)
        ).fetchall()
    sbl_institution_type_expected = data_feed_migration_helper(sbl_institution_type_tablename)
    assert sbl_institution_type_rows == sbl_institution_type_expected
