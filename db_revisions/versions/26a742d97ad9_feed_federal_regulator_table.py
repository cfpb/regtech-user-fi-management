"""Feed Federal Regulator table

Revision ID: 26a742d97ad9
Revises: 7b6ff51002b5
Create Date: 2023-12-14 01:23:17.872728

"""
from typing import Sequence, Union
from alembic import op
from entities.models import FederalRegulatorDao
from config import federal_regulator_feed


# revision identifiers, used by Alembic.
revision: str = "26a742d97ad9"
down_revision: Union[str, None] = "7b6ff51002b5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.bulk_insert(FederalRegulatorDao.__table__, federal_regulator_feed)


def downgrade() -> None:
    op.execute(FederalRegulatorDao.__table__.delete())
