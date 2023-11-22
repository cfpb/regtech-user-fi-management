"""Create financial_institution_domains table

Revision ID: 20e0d51d8be9
Revises: f76c5004993f
Create Date: 2023-11-02 11:37:52.487064

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from db_revisions.utils import table_exists


# revision identifiers, used by Alembic.
revision: str = "20e0d51d8be9"
down_revision: Union[str, None] = "f76c5004993f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on = ["f76c5004993f"]


def upgrade() -> None:
    if not table_exists("financial_institution_domains"):
        op.create_table(
            "financial_institution_domains",
            sa.Column("domain", sa.String(), nullable=False),
            sa.Column("lei", sa.String(), nullable=False),
            sa.Column("event_time", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
            sa.ForeignKeyConstraint(
                ["lei"],
                ["financial_institutions.lei"],
            ),
            sa.PrimaryKeyConstraint("domain", "lei"),
        )
        op.create_index(
            op.f("ix_financial_institution_domains_domain"), "financial_institution_domains", ["domain"], unique=False
        )
        op.create_index(
            op.f("ix_financial_institution_domains_lei"), "financial_institution_domains", ["lei"], unique=False
        )


def downgrade() -> None:
    op.drop_table("financial_institution_domains")
