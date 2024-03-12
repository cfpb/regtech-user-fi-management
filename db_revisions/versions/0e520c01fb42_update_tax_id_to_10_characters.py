"""update tax-id to 10 characters

Revision ID: 0e520c01fb42
Revises: 8106d83ff594
Create Date: 2024-03-12 11:40:25.790658

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0e520c01fb42"
down_revision: Union[str, None] = "8106d83ff594"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("financial_institutions") as batch_op:
        batch_op.alter_column("tax_id", existing_type=sa.String(9), type_=sa.String(10))
    with op.batch_alter_table("financial_institutions_history") as batch_op:
        batch_op.alter_column("tax_id", existing_type=sa.String(9), type_=sa.String(10))


def downgrade() -> None:
    with op.batch_alter_table("financial_institutions") as batch_op:
        batch_op.alter_column("tax_id", existing_type=sa.String(10), type_=sa.String(9))
    with op.batch_alter_table("financial_institutions_history") as batch_op:
        batch_op.alter_column("tax_id", existing_type=sa.String(10), type_=sa.String(9))
