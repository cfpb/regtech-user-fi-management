"""240111 add free form text for sbl types

Revision ID: 6826f05140cd
Revises: ada681e1877f
Create Date: 2024-01-11 14:33:56.518611

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6826f05140cd"
down_revision: Union[str, None] = "ada681e1877f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("fi_to_type_mapping", sa.Column("details", type_=sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("fi_to_type_mapping", "details")
