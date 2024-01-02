"""Seed HMDA Institution Type table

Revision ID: f4ff7d1aa6df
Revises: 26a742d97ad9
Create Date: 2023-12-14 01:23:47.017878

"""
from typing import Sequence, Union
from alembic import op
from sqlalchemy import MetaData, Table


# revision identifiers, used by Alembic.
revision: str = "f4ff7d1aa6df"
down_revision: Union[str, None] = "26a742d97ad9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    seed_data = [
        {"id": "1", "name": "National Bank (OCC supervised)"},
        {"id": "2", "name": "State Member Bank (FRS Supervised)"},
        {"id": "3", "name": "State non-member bank (FDIC supervised)"},
        {"id": "4", "name": "State Chartered Thrift (FDIC supervised)"},
        {"id": "5", "name": "Federal Chartered Thrift (OCC supervised)"},
        {"id": "6", "name": "Credit Union (NCUA supervised)"},
        {"id": "7", "name": "Federal Branch or Agency of Foreign Banking Organization (FBO)"},
        {"id": "8", "name": "Branch or Agency of FBO (FRS supervised)"},
        {"id": "9", "name": "MBS of national Bank (OCC supervised)"},
        {"id": "10", "name": "MBS of state member bank (FRS supervised)"},
        {"id": "11", "name": "MBS of state non-member bank (FDIC supervised)"},
        {"id": "12", "name": "MBS of Bank Holding Company (BHC) (FRS supervised)"},
        {"id": "13", "name": "MBS of credit union (NCUA supervised)"},
        {"id": "14", "name": "independent MBS, no depository affiliation"},
        {"id": "15", "name": "MBS of Savings and Loan Holding Co"},
        {"id": "16", "name": "MBS of state chartered Thrift"},
        {"id": "17", "name": "MBS of federally chartered thrift (OCC supervised)"},
        {"id": "18", "name": "Affiliate of depository institution. MBS is in the same ownership org as a depository."},
    ]
    meta = MetaData()
    meta.reflect(op.get_bind())
    table = Table("hmda_institution_type", meta)

    op.bulk_insert(table, seed_data)


def downgrade() -> None:
    meta = MetaData()
    meta.reflect(op.get_bind())
    table = Table("hmda_institution_type", meta)

    op.execute(table.delete())
