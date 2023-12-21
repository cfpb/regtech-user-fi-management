"""Feed SBL Institution Type table

Revision ID: a41281b1e109
Revises: f4ff7d1aa6df
Create Date: 2023-12-14 01:24:00.120073

"""
from typing import Sequence, Union
from alembic import op
from entities.models import SBLInstitutionTypeDao
from config import sbl_institution_type_feed

# revision identifiers, used by Alembic.
revision: str = "a41281b1e109"
down_revision: Union[str, None] = "f4ff7d1aa6df"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.bulk_insert(SBLInstitutionTypeDao.__table__, sbl_institution_type_feed)


def downgrade() -> None:
    op.execute(SBLInstitutionTypeDao.__table__.delete())
