import os
import csv
from sqlalchemy import select
from sqlalchemy.engine import Engine
from pytest_alembic import MigrationContext
from entities.models import AddressStateDao, FederalRegulatorDao, HMDAInstitutionTypeDao, SBLInstitutionTypeDao


def data_feed_helper(table_name):
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
    alembic_runner.migrate_up_one()

    with alembic_engine.connect() as conn:
        address_state_rows = conn.execute(select(AddressStateDao.code, AddressStateDao.name)).fetchall()
    address_state_expected = data_feed_helper(AddressStateDao.__tablename__)
    assert address_state_rows == address_state_expected


def test_federal_regulator_data_feed(alembic_runner: MigrationContext, alembic_engine: Engine):
    # Migrate up to, but not including this new migration
    alembic_runner.migrate_up_before("26a742d97ad9")

    # Test federal_regulator feed
    alembic_runner.migrate_up_one()
    with alembic_engine.connect() as conn:
        federal_regulator_rows = conn.execute(select(FederalRegulatorDao.id, FederalRegulatorDao.name)).fetchall()
    federal_regulator_expected = data_feed_helper(FederalRegulatorDao.__tablename__)
    assert federal_regulator_rows == federal_regulator_expected


def test_hmda_institution_type_data_feed(alembic_runner: MigrationContext, alembic_engine: Engine):
    # Migrate up to, but not including this new migration
    alembic_runner.migrate_up_before("f4ff7d1aa6df")

    # Test hmda_institution_type feed
    alembic_runner.migrate_up_one()
    with alembic_engine.connect() as conn:
        hmda_institution_type_rows = conn.execute(
            select(HMDAInstitutionTypeDao.id, HMDAInstitutionTypeDao.name)
        ).fetchall()
    hmda_institution_type_expected = data_feed_helper(HMDAInstitutionTypeDao.__tablename__)
    assert hmda_institution_type_rows == hmda_institution_type_expected


def test_sbl_institution_type_data_feed(alembic_runner: MigrationContext, alembic_engine: Engine):
    # Migrate up to, but not including this new migration
    alembic_runner.migrate_up_before("a41281b1e109")

    # Test sbl_institution_type feed
    alembic_runner.migrate_up_one()
    with alembic_engine.connect() as conn:
        sbl_institution_type_rows = conn.execute(
            select(SBLInstitutionTypeDao.id, SBLInstitutionTypeDao.name)
        ).fetchall()
    sbl_institution_type_expected = data_feed_helper(SBLInstitutionTypeDao.__tablename__)
    assert sbl_institution_type_rows == sbl_institution_type_expected
