"""240131 fi type association history table

Revision ID: 8106d83ff594
Revises: 329c70502325
Create Date: 2024-01-31 10:23:21.163572

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8106d83ff594"
down_revision: Union[str, None] = "329c70502325"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "fi_to_type_mapping_history",
        sa.Column("version", sa.Integer()),
        sa.Column("fi_id", sa.String(), nullable=False),
        sa.Column("type_id", sa.String(), nullable=False),
        sa.Column("details", sa.String()),
        sa.Column("modified_by", sa.String()),
        sa.Column("event_time", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("changeset", sa.JSON),
        sa.PrimaryKeyConstraint("fi_id", "type_id", "version"),
    )


def downgrade() -> None:
    op.drop_table("fi_to_type_mapping_history")
