"""Replace is_active with lei_status in financial_institutions table

Revision ID: 6613e1e2c133
Revises: 6dd77f09fae6
Create Date: 2024-11-13 00:43:53.489086

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from db_revisions.utils import table_exists, get_table_by_name, get_indices_from_collection


# revision identifiers, used by Alembic.
revision: str = "6613e1e2c133"
down_revision: Union[str, None] = "6dd77f09fae6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

lei_status_seed_data = [
    {"code": "ISSUED", "name": "Issued", "can_file": True},
    {"code": "LAPSED", "name": "Lapsed", "can_file": False},
    {"code": "RETIRED", "name": "Retired", "can_file": False},
]


def upgrade() -> None:

    # Creating lei_status table
    if not table_exists("lei_status"):
        op.create_table(
            "lei_status",
            sa.Column("code", sa.String(), nullable=False),
            sa.Column("name", sa.String(), nullable=False),
            sa.Column("can_file", sa.Boolean(), nullable=False),
            sa.Column("event_time", sa.DateTime(), server_default=sa.func.now(), nullable=False),
            sa.PrimaryKeyConstraint("code"),
            sa.UniqueConstraint("name"),
        )

    # Seeding lei_status table
    lei_status_table = get_table_by_name("lei_status")
    op.bulk_insert(lei_status_table, lei_status_seed_data)

    # Removing is_active from and adding lei_status_code to financial_institutions table
    op.add_column("financial_institutions", sa.Column("lei_status_code", sa.String(), nullable=True))

    op.execute(
        "UPDATE financial_institutions SET lei_status_code = CASE is_active WHEN True THEN 'ISSUED' ELSE 'LAPSED' END"
    )

    with op.batch_alter_table("financial_institutions") as batch_op:
        batch_op.alter_column("lei_status_code", existing_nullable=True, nullable=False)
        batch_op.create_index(
            index_name=batch_op.f("ix_financial_institutions_lei_status_code"),
            columns=["lei_status_code"],
            unique=False,
        )
        batch_op.create_foreign_key(
            "fk_lei_status_financial_institutions",
            "lei_status",
            ["lei_status_code"],
            ["code"],
        )

        batch_op.drop_index(index_name="ix_financial_institutions_is_active")
        batch_op.drop_column("is_active")

    # Removing is_active from and adding lei_status_code to financial_institutions_history table
    op.add_column("financial_institutions_history", sa.Column("lei_status_code", sa.String()))


def downgrade() -> None:

    op.drop_column("financial_institutions_history", "lei_status_code")

    op.add_column(
        "financial_institutions",
        sa.Column(name="is_active", type_=sa.Boolean(), nullable=True),
    )
    op.execute(
        "UPDATE financial_institutions SET is_active = CASE lei_status_code WHEN 'ISSUED' THEN True ELSE False END"
    )

    with op.batch_alter_table("financial_institutions") as batch_op:
        batch_op.alter_column("is_active", existing_nullable=True, nullable=False)
        batch_op.create_index(
            index_name=batch_op.f("ix_financial_institutions_is_active"), columns=["is_active"], unique=False
        )

        batch_op.drop_constraint(constraint_name="fk_lei_status_financial_institutions")
        batch_op.drop_index("ix_financial_institutions_lei_status_code")
        batch_op.drop_column("lei_status_code")

    lei_status_table = get_table_by_name("lei_status")
    codes = get_indices_from_collection(lei_status_seed_data, "code")
    op.execute(lei_status_table.delete().where(lei_status_table.c.code.in_(codes)))

    op.drop_table("lei_status")
