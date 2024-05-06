"""Create Federal Regulator Table

Revision ID: 549c612bf1c9
Revises: "8b1ba6a3275b"
Create Date: 2023-11-29 12:09:20.012400

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from db_revisions.utils import table_exists


# revision identifiers, used by Alembic.
revision: str = "549c612bf1c9"
down_revision: Union[str, None] = "8b1ba6a3275b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    if not table_exists("federal_regulator"):
        op.create_table(
            "federal_regulator",
            sa.Column("id", sa.String(length=4), nullable=False),
            sa.Column("name", sa.String(), nullable=False),
            sa.Column("event_time", sa.DateTime(), server_default=sa.func.now(), nullable=False),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("name"),
        )


def downgrade() -> None:
    op.drop_table("federal_regulator")
