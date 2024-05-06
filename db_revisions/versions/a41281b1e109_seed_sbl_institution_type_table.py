"""Seed SBL Institution Type table

Revision ID: a41281b1e109
Revises: f4ff7d1aa6df
Create Date: 2023-12-14 01:24:00.120073

"""

from typing import Sequence, Union
from alembic import op
from db_revisions.utils import get_table_by_name, get_indices_from_collection

# revision identifiers, used by Alembic.
revision: str = "a41281b1e109"
down_revision: Union[str, None] = "f4ff7d1aa6df"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

seed_data = [
    {"id": "1", "name": "Bank or savings association"},
    {"id": "2", "name": "Minority depository institution"},
    {"id": "3", "name": "Credit union"},
    {"id": "4", "name": "Nondepository institution"},
    {"id": "5", "name": "Community development financial institution (CDFI)"},
    {"id": "6", "name": "Other nonprofit financial institution"},
    {"id": "7", "name": "Farm Credit System institution"},
    {"id": "8", "name": "Government lender"},
    {"id": "9", "name": "Commercial finance company"},
    {"id": "10", "name": "Equipment finance company"},
    {"id": "11", "name": "Industrial loan company"},
    {"id": "12", "name": "Online lender"},
    {"id": "13", "name": "Other"},
]


def upgrade() -> None:
    table = get_table_by_name("sbl_institution_type")

    op.bulk_insert(table, seed_data)


def downgrade() -> None:
    table = get_table_by_name("sbl_institution_type")

    ids = get_indices_from_collection(seed_data, "id")

    op.execute(table.delete().where(table.c.id.in_(ids)))
