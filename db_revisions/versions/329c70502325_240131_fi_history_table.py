"""240131 fi history table

Revision ID: 329c70502325
Revises: 3f893e52d05c
Create Date: 2024-01-31 10:23:01.081439

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "329c70502325"
down_revision: Union[str, None] = "3f893e52d05c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "financial_institutions_history",
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("lei", sa.String(), nullable=False),
        sa.Column("name", sa.String()),
        sa.Column("is_active", sa.Boolean()),
        sa.Column("tax_id", sa.String(9)),
        sa.Column("rssd_id", sa.Integer()),
        sa.Column("primary_federal_regulator_id", sa.String(4)),
        sa.Column("hmda_institution_type_id", sa.String()),
        sa.Column("hq_address_street_1", sa.String()),
        sa.Column("hq_address_street_2", sa.String()),
        sa.Column("hq_address_city", sa.String()),
        sa.Column("hq_address_state_code", sa.String(2)),
        sa.Column("hq_address_zip", sa.String(5)),
        sa.Column("parent_lei", sa.String(20)),
        sa.Column("parent_legal_name", sa.String()),
        sa.Column("parent_rssd_id", sa.Integer()),
        sa.Column("top_holder_lei", sa.String(20)),
        sa.Column("top_holder_legal_name", sa.String()),
        sa.Column("top_holder_rssd_id", sa.Integer()),
        sa.Column("event_time", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("modified_by", sa.String()),
        sa.Column("changeset", sa.JSON),
        sa.PrimaryKeyConstraint("lei", "version"),
    )


def downgrade() -> None:
    op.drop_table("financial_institutions_history")
