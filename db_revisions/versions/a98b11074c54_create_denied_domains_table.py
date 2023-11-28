"""Create denied_domains table

Revision ID: a98b11074c54
Revises: 
Create Date: 2023-11-02 11:31:54.882727

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from db_revisions.utils import table_exists


# revision identifiers, used by Alembic.
revision: str = "a98b11074c54"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    if not table_exists("denied_domains"):
        op.create_table(
            "denied_domains",
            sa.Column("domain", sa.String(), nullable=False),
            sa.Column("event_time", sa.DateTime(), server_default=sa.func.now(), nullable=False),
            sa.PrimaryKeyConstraint("domain"),
        )
        op.create_index(op.f("ix_denied_domains_domain"), "denied_domains", ["domain"], unique=False)


def downgrade() -> None:
    op.drop_table("denied_domains")
