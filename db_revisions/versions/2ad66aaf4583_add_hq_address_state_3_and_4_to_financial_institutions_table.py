"""add hq_address_state_3 and hq_address_state_3 fields to financial_institutions table

Revision ID: 2ad66aaf4583
Revises: d6e4a13fbebd
Create Date: 2024-04-09 00:17:23.263719

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2ad66aaf4583"
down_revision: Union[str, None] = "d6e4a13fbebd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("financial_institutions") as batch_op:
        batch_op.add_column(sa.Column("hq_address_street_3", sa.String, nullable=True))
        batch_op.add_column(sa.Column("hq_address_street_4", sa.String, nullable=True))


def downgrade() -> None:
    with op.batch_alter_table("financial_institutions") as batch_op:
        batch_op.drop_column("hq_address_street_3")
        batch_op.drop_column("hq_address_street_4")
