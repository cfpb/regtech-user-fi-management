"""Seed Federal Regulator table

Revision ID: 26a742d97ad9
Revises: 7b6ff51002b5
Create Date: 2023-12-14 01:23:17.872728

"""
from typing import Sequence, Union
from alembic import op
from entities.models.dao import Base


# revision identifiers, used by Alembic.
revision: str = "26a742d97ad9"
down_revision: Union[str, None] = "7b6ff51002b5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

federal_regulator_table = Base.metadata.tables.get("federal_regulator")


def upgrade() -> None:
    seed_data = [
        {"id": "FCA", "name": "Farm Credit Administration"},
        {"id": "FDIC", "name": "Federal Deposit Insurance Corporation"},
        {"id": "FHFA", "name": "Federal Housing Finance Agency"},
        {"id": "FRS", "name": "Federal Reserve System"},
        {"id": "NCUA", "name": "National Credit Union Administration"},
        {"id": "OCC", "name": "Office of the Comptroller of the Currency"},
        {"id": "OTS", "name": "Office of Thrift Supervision (only valid until July 21, 2011)"},
    ]
    op.bulk_insert(federal_regulator_table, seed_data)


def downgrade() -> None:
    op.execute(federal_regulator_table.delete())
