"""add char limit to financial institution table fields

Revision ID: 6dd77f09fae6
Revises: 2ad66aaf4583
Create Date: 2024-11-05 09:28:35.233356

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6dd77f09fae6"
down_revision: Union[str, None] = "2ad66aaf4583"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("financial_institutions", schema=None) as batch_op:
        batch_op.alter_column("name", type_=sa.String(255), nullable=False)
        batch_op.alter_column("hq_address_street_1", type_=sa.String(255), nullable=False)
        batch_op.alter_column("hq_address_street_2", type_=sa.String(255), nullable=True)
        batch_op.alter_column("hq_address_street_3", type_=sa.String(255), nullable=True)
        batch_op.alter_column("hq_address_street_4", type_=sa.String(255), nullable=True)
        batch_op.alter_column("hq_address_city", type_=sa.String(255), nullable=False)
        batch_op.alter_column("parent_legal_name", type_=sa.String(255), nullable=True)
        batch_op.alter_column("top_holder_legal_name", type_=sa.String(255), nullable=True)


def downgrade() -> None:
    with op.batch_alter_table("financial_institutions", schema=None) as batch_op:
        batch_op.alter_column("name", type_=sa.String, nullable=False)
        batch_op.alter_column("hq_address_street_1", type_=sa.String, nullable=False)
        batch_op.alter_column("hq_address_street_2", type_=sa.String, nullable=True)
        batch_op.alter_column("hq_address_street_3", type_=sa.String, nullable=True)
        batch_op.alter_column("hq_address_street_4", type_=sa.String, nullable=True)
        batch_op.alter_column("hq_address_city", type_=sa.String, nullable=False)
        batch_op.alter_column("parent_legal_name", type_=sa.String, nullable=True)
        batch_op.alter_column("top_holder_legal_name", type_=sa.String, nullable=True)
