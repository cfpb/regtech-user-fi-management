"""Seed SBL Institution Type table

Revision ID: a41281b1e109
Revises: f4ff7d1aa6df
Create Date: 2023-12-14 01:24:00.120073

"""
from typing import Sequence, Union
from alembic import op
from entities.models.dao import Base

# revision identifiers, used by Alembic.
revision: str = "a41281b1e109"
down_revision: Union[str, None] = "f4ff7d1aa6df"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

sbl_institution_type_table = Base.metadata.tables.get("sbl_institution_type")


def upgrade() -> None:
    seed_data = [
        {"id": "1", "name": "Bank or savings association."},
        {"id": "2", "name": "Minority depository institution."},
        {"id": "3", "name": "Credit union."},
        {"id": "4", "name": "Nondepository institution."},
        {"id": "5", "name": "Community development financial institution (CDFI)."},
        {"id": "6", "name": "Other nonprofit financial institution."},
        {"id": "7", "name": "Farm Credit System institution."},
        {"id": "8", "name": "Government lender."},
        {"id": "9", "name": "Commercial finance company."},
        {"id": "10", "name": "Equipment finance company."},
        {"id": "11", "name": "Industrial loan company."},
        {"id": "12", "name": "Online lender."},
        {"id": "13", "name": "Other"},
    ]
    op.bulk_insert(sbl_institution_type_table, seed_data)


def downgrade() -> None:
    op.execute(sbl_institution_type_table.delete())
