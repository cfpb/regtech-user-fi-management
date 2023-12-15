"""Feed Address State table

Revision ID: 7b6ff51002b5
Revises: 045aa502e050
Create Date: 2023-12-14 01:21:48.325752

"""
from typing import Sequence, Union
from alembic import op
from db_revisions.utils import get_feed_data_from_file
from entities.models import AddressStateDao


# revision identifiers, used by Alembic.
revision: str = "7b6ff51002b5"
down_revision: Union[str, None] = "045aa502e050"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    data = get_feed_data_from_file("address_state")

    op.bulk_insert(AddressStateDao.__table__, data)


def downgrade() -> None:
    op.execute(AddressStateDao.__table__.delete())
