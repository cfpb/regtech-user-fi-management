"""240130 add version

Revision ID: 3f893e52d05c
Revises: 6826f05140cd
Create Date: 2024-01-30 14:37:47.652233

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3f893e52d05c"
down_revision: Union[str, None] = "6826f05140cd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("financial_institutions") as batch_op:
        batch_op.add_column(sa.Column("version", type_=sa.Integer(), nullable=False, server_default=sa.text("1")))
        batch_op.add_column(sa.Column("modified_by", sa.String()))
    with op.batch_alter_table("fi_to_type_mapping") as batch_op:
        batch_op.add_column(sa.Column("version", type_=sa.Integer(), nullable=False, server_default=sa.text("1")))
        batch_op.add_column(sa.Column("modified_by", sa.String()))


def downgrade() -> None:
    op.drop_column("financial_institutions", "version")
    op.drop_column("financial_institutions", "modified_by")
    op.drop_column("fi_to_type_mapping", "version")
    op.drop_column("fi_to_type_mapping", "modified_by")
