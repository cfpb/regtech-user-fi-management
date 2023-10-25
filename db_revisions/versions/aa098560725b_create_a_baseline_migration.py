"""Create a baseline migration

Revision ID: aa098560725b
Revises: 
Create Date: 2023-10-25 10:07:38.214272

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "aa098560725b"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "denied_domains",
        sa.Column("domain", sa.String(), nullable=False),
        sa.Column("event_time", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("domain"),
    )
    op.create_index(op.f("ix_denied_domains_domain"), "denied_domains", ["domain"], unique=False)
    op.create_table(
        "financial_institutions",
        sa.Column("lei", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("event_time", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("lei"),
    )
    op.create_index(op.f("ix_financial_institutions_lei"), "financial_institutions", ["lei"], unique=True)
    op.create_index(op.f("ix_financial_institutions_name"), "financial_institutions", ["name"], unique=False)
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
    op.drop_table("financial_institutions")
    op.drop_table("denied_domains")
