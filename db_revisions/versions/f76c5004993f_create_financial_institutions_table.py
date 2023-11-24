"""Create financial_institutions table

Revision ID: f76c5004993f
Revises: a98b11074c54
Create Date: 2023-11-02 11:34:43.808166

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from db_revisions.utils import table_exists


# revision identifiers, used by Alembic.
revision: str = "f76c5004993f"
down_revision: Union[str, None] = "a98b11074c54"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    if not table_exists("financial_institutions"):
        op.create_table(
            "financial_institutions",
            sa.Column("lei", sa.String(), nullable=False),
            sa.Column("name", sa.String(), nullable=False),
            sa.Column("event_time", sa.DateTime(), server_default=sa.func.now(), nullable=False),
            sa.PrimaryKeyConstraint("lei"),
        )
        op.create_index(op.f("ix_financial_institutions_lei"), "financial_institutions", ["lei"], unique=True)
        op.create_index(op.f("ix_financial_institutions_name"), "financial_institutions", ["name"], unique=False)


def downgrade() -> None:
    op.drop_table("financial_institutions")
