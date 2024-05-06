"""Seed Address State table

Revision ID: 7b6ff51002b5
Revises: 045aa502e050
Create Date: 2023-12-14 01:21:48.325752

"""

from typing import Sequence, Union
from alembic import op
from db_revisions.utils import get_table_by_name, get_indices_from_collection


# revision identifiers, used by Alembic.
revision: str = "7b6ff51002b5"
down_revision: Union[str, None] = "045aa502e050"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

seed_data = [
    {"code": "AL", "name": "Alabama"},
    {"code": "AK", "name": "Alaska"},
    {"code": "AZ", "name": "Arizona"},
    {"code": "AR", "name": "Arkansas"},
    {"code": "CA", "name": "California"},
    {"code": "CO", "name": "Colorado"},
    {"code": "CT", "name": "Connecticut"},
    {"code": "DE", "name": "Delaware"},
    {"code": "FL", "name": "Florida"},
    {"code": "GA", "name": "Georgia"},
    {"code": "HI", "name": "Hawaii"},
    {"code": "ID", "name": "Idaho"},
    {"code": "IL", "name": "Illinois"},
    {"code": "IN", "name": "Indiana"},
    {"code": "IA", "name": "Iowa"},
    {"code": "KS", "name": "Kansas"},
    {"code": "KY", "name": "Kentucky"},
    {"code": "LA", "name": "Louisiana"},
    {"code": "ME", "name": "Maine"},
    {"code": "MD", "name": "Maryland"},
    {"code": "MA", "name": "Massachusetts"},
    {"code": "MI", "name": "Michigan"},
    {"code": "MN", "name": "Minnesota"},
    {"code": "MS", "name": "Mississippi"},
    {"code": "MO", "name": "Missouri"},
    {"code": "MT", "name": "Montana"},
    {"code": "NE", "name": "Nebraska"},
    {"code": "NV", "name": "Nevada"},
    {"code": "NH", "name": "New Hampshire"},
    {"code": "NJ", "name": "New Jersey"},
    {"code": "NM", "name": "New Mexico"},
    {"code": "NY", "name": "New York"},
    {"code": "NC", "name": "North Carolina"},
    {"code": "ND", "name": "North Dakota"},
    {"code": "OH", "name": "Ohio"},
    {"code": "OK", "name": "Oklahoma"},
    {"code": "OR", "name": "Oregon"},
    {"code": "PA", "name": "Pennsylvania"},
    {"code": "RI", "name": "Rhode Island"},
    {"code": "SC", "name": "South Carolina"},
    {"code": "SD", "name": "South Dakota"},
    {"code": "TN", "name": "Tennessee"},
    {"code": "TX", "name": "Texas"},
    {"code": "UT", "name": "Utah"},
    {"code": "VT", "name": "Vermont"},
    {"code": "VA", "name": "Virginia"},
    {"code": "WA", "name": "Washington"},
    {"code": "WV", "name": "West Virginia"},
    {"code": "WI", "name": "Wisconsin"},
    {"code": "WY", "name": "Wyoming"},
    {"code": "DC", "name": "District of Columbia"},
    {"code": "AS", "name": "American Samoa"},
    {"code": "GU", "name": "Guam"},
    {"code": "MP", "name": "Northern Mariana Islands"},
    {"code": "PR", "name": "Puerto Rico"},
    {"code": "UM", "name": "United States Minor Outlying Islands"},
    {"code": "VI", "name": "Virgin Islands, U.S."},
]


def upgrade() -> None:
    table = get_table_by_name("address_state")

    op.bulk_insert(table, seed_data)


def downgrade() -> None:
    table = get_table_by_name("address_state")

    codes = get_indices_from_collection(seed_data, "code")

    op.execute(table.delete().where(table.c.code.in_(codes)))
