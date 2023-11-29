"""Create HMDA Institution Type Table

Revision ID: 8b1ba6a3275b
Revises: 20e0d51d8be9
Create Date: 2023-11-29 12:14:16.694281

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8b1ba6a3275b"
down_revision: Union[str, None] = "20e0d51d8be9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "hmda_institution_type",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("event_time", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_hmda_institution_type_id"), "hmda_institution_type", ["id"], unique=False)


def downgrade() -> None:
    op.drop_table("hmda_institution_type")
