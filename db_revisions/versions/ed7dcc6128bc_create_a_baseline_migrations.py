"""Create a baseline migrations

Revision ID: ed7dcc6128bc
Revises: 
Create Date: 2023-10-18 11:13:57.509078

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ed7dcc6128bc"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    denied_domains = op.create_table(
        "denied_domains",
        sa.Column("domain", sa.String(), nullable=False),
        sa.Column("event_time", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.PrimaryKeyConstraint("domain", name="denied_domains_pkey"),
    )
    op.create_index("ix_denied_domains_domain", "denied_domains", ["domain"], unique=True)
    op.bulk_insert(denied_domains, [{"domain": "gmail.com"}, {"domain": "yahoo.com"}, {"domain": "aol.com"}])

    financial_institutions = op.create_table(
        "financial_institutions",
        sa.Column("lei", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("event_time", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.PrimaryKeyConstraint("lei", name="financial_institutions_pkey"),
    )
    op.create_index("ix_financial_institutions_lei", "financial_institutions", ["lei"], unique=True)
    op.create_index("ix_financial_institutions_name", "financial_institutions", ["name"], unique=False)
    op.bulk_insert(
        financial_institutions,
        [
            {"lei": "TEST1LEI", "name": "Test 1"},
            {"lei": "TEST2LEI", "name": "Test 2"},
            {"lei": "TEST3LEI", "name": "Test 3"},
        ],
    )

    financial_institutions_domains = op.create_table(
        "financial_institutions_domains",
        sa.Column("domain", sa.String(), nullable=False),
        sa.Column("lei", sa.String(), nullable=False),
        sa.Column("event_time", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(
            ["lei"],
            ["financial_institutions.lei"],
        ),
        sa.PrimaryKeyConstraint("domain", "lei", name="financial_institution_domains_pkey"),
    )
    op.create_index(
        "ix_financial_institution_domains_domain", "financial_institutions_domains", ["domain"], unique=False
    )
    op.create_index("ix_financial_institution_domains_lei", "financial_institutions_domains", ["lei"], unique=False)
    op.bulk_insert(
        financial_institutions_domains,
        [
            {"domain": "test1.local", "lei": "TEST1LEI"},
            {"domain": "test2.local", "lei": "TEST2LEI"},
            {"domain": "test3.local", "lei": "TEST3LEI"},
        ],
    )


def downgrade() -> None:
    op.drop_table("financial_institutions_domains")

    op.drop_table("financial_institutions")

    op.drop_table("denied_domains")
