"""Feed HMDA Institution Type table

Revision ID: f4ff7d1aa6df
Revises: 26a742d97ad9
Create Date: 2023-12-14 01:23:47.017878

"""
from typing import Sequence, Union
from alembic import op
from db_revisions.utils import get_feed_data_from_file
from entities.models import HMDAInstitutionTypeDao


# revision identifiers, used by Alembic.
revision: str = "f4ff7d1aa6df"
down_revision: Union[str, None] = "26a742d97ad9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    data = get_feed_data_from_file("hmda_institution_type")

    op.bulk_insert(HMDAInstitutionTypeDao.__table__, data)


def downgrade() -> None:
    op.execute(HMDAInstitutionTypeDao.__table__.delete())
