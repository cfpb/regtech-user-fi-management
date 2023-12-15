"""Feed Federal Regulator table

Revision ID: 26a742d97ad9
Revises: 7b6ff51002b5
Create Date: 2023-12-14 01:23:17.872728

"""
from typing import Sequence, Union
from alembic import op
from db_revisions.utils import get_feed_data_from_file
from entities.models import FederalRegulatorDao


# revision identifiers, used by Alembic.
revision: str = "26a742d97ad9"
down_revision: Union[str, None] = "7b6ff51002b5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    data = get_feed_data_from_file("federal_regulator")

    op.bulk_insert(FederalRegulatorDao.__table__, data)


def downgrade() -> None:
    op.execute(FederalRegulatorDao.__table__.delete())
