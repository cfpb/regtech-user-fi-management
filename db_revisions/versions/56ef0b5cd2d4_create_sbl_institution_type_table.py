"""Create SBL Institution Type Table

Revision ID: 56ef0b5cd2d4
Revises: "1f6c33f20a2e"
Create Date: 2023-11-29 12:20:05.593826

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from db_revisions.utils import table_exists


# revision identifiers, used by Alembic.
revision: str = "56ef0b5cd2d4"
down_revision: Union[str, None] = "1f6c33f20a2e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    if not table_exists("sbl_institution_type"):
        op.create_table(
            "sbl_institution_type",
            sa.Column("id", sa.String(), nullable=False),
            sa.Column("name", sa.String(), nullable=False),
            sa.Column("event_time", sa.DateTime(), server_default=sa.func.now(), nullable=False),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("name"),
        )
        op.create_index(op.f("ix_sbl_institution_type_id"), "sbl_institution_type", ["id"], unique=False)


def downgrade() -> None:
    op.drop_table("sbl_institution_type")
