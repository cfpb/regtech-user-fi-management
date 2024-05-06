"""231227 add active field to institutions table

Revision ID: 383ab402c8c2
Revises: a41281b1e109
Create Date: 2023-12-27 14:21:33.567414

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "383ab402c8c2"
down_revision: Union[str, None] = "a41281b1e109"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("financial_institutions") as batch_op:
        batch_op.add_column(sa.Column(name="is_active", type_=sa.Boolean(), nullable=False, server_default=sa.true()))
        batch_op.create_index(
            index_name=batch_op.f("ix_financial_institutions_is_active"), columns=["is_active"], unique=False
        )


def downgrade() -> None:
    op.drop_index(index_name="ix_financial_institutions_is_active", table_name="financial_institutions")
    op.drop_column(table_name="financial_institutions", column_name="is_active")
