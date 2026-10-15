"""initial migration - create transactions and budgets tables

Revision ID: 001_initial
Revises: 
Create Date: 2026-10-16 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    is_pg = bind.dialect.name == "postgresql"

    # Safely create enum types in PostgreSQL if they don't already exist
    if is_pg:
        op.execute(sa.text("""
            DO $$ BEGIN
                CREATE TYPE transactiontype AS ENUM ('income', 'expense');
            EXCEPTION
                WHEN duplicate_object THEN null;
            END $$;
        """))
        op.execute(sa.text("""
            DO $$ BEGIN
                CREATE TYPE transactioncategory AS ENUM (
                    'salary', 'freelance', 'investment',
                    'food', 'transport', 'housing', 'utilities',
                    'entertainment', 'healthcare', 'education', 'shopping', 'other'
                );
            EXCEPTION
                WHEN duplicate_object THEN null;
            END $$;
        """))

    # Create budgets table
    op.create_table(
        "budgets",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("category", sa.String(length=50), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("month", sa.Integer(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_budgets_category"), "budgets", ["category"], unique=False)
    op.create_index(op.f("ix_budgets_id"), "budgets", ["id"], unique=False)

    type_col = (
        postgresql.ENUM("income", "expense", name="transactiontype", create_type=False)
        if is_pg
        else sa.Enum("income", "expense", name="transactiontype")
    )
    category_col = (
        postgresql.ENUM(
            "salary", "freelance", "investment",
            "food", "transport", "housing", "utilities",
            "entertainment", "healthcare", "education", "shopping", "other",
            name="transactioncategory",
            create_type=False
        )
        if is_pg
        else sa.Enum(
            "salary", "freelance", "investment",
            "food", "transport", "housing", "utilities",
            "entertainment", "healthcare", "education", "shopping", "other",
            name="transactioncategory"
        )
    )

    # Create transactions table
    op.create_table(
        "transactions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("transaction_type", type_col, nullable=False),
        sa.Column("category", category_col, nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_recurring", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_transactions_category"), "transactions", ["category"], unique=False)
    op.create_index(op.f("ix_transactions_date"), "transactions", ["date"], unique=False)
    op.create_index(op.f("ix_transactions_id"), "transactions", ["id"], unique=False)
    op.create_index(op.f("ix_transactions_transaction_type"), "transactions", ["transaction_type"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_transactions_transaction_type"), table_name="transactions")
    op.drop_index(op.f("ix_transactions_id"), table_name="transactions")
    op.drop_index(op.f("ix_transactions_date"), table_name="transactions")
    op.drop_index(op.f("ix_transactions_category"), table_name="transactions")
    op.drop_table("transactions")
    op.drop_index(op.f("ix_budgets_id"), table_name="budgets")
    op.drop_index(op.f("ix_budgets_category"), table_name="budgets")
    op.drop_table("budgets")

    # Drop enums
    sa.Enum(name="transactioncategory").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="transactiontype").drop(op.get_bind(), checkfirst=True)
