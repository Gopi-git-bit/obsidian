"""Add local user accounts for JWT RBAC.

Revision ID: 004_auth_rbac_foundation
Revises: 003_order_to_settlement_flow
Create Date: 2026-06-01
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "004_auth_rbac_foundation"
down_revision = "003_order_to_settlement_flow"
branch_labels = None
depends_on = None

USER_ROLE_VALUES = (
    "CUSTOMER",
    "DRIVER",
    "TRANSPORT_COMPANY",
    "SUPPORT_ADMIN",
    "OPS_ADMIN",
    "FINANCE_ADMIN",
    "SUPER_ADMIN",
)


def _user_role_enum(bind):
    if bind.dialect.name == "postgresql":
        return postgresql.ENUM(*USER_ROLE_VALUES, name="userrole", create_type=False)
    return sa.Enum(*USER_ROLE_VALUES, name="userrole")


def upgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        op.execute(
            """
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'userrole') THEN
                    CREATE TYPE userrole AS ENUM (
                        'CUSTOMER',
                        'DRIVER',
                        'TRANSPORT_COMPANY',
                        'SUPPORT_ADMIN',
                        'OPS_ADMIN',
                        'FINANCE_ADMIN',
                        'SUPER_ADMIN'
                    );
                END IF;
            END
            $$;
            """
        )
    else:
        sa.Enum(*USER_ROLE_VALUES, name="userrole").create(bind, checkfirst=True)

    user_role = _user_role_enum(bind)

    op.create_table(
        "user_accounts",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("username", sa.String(length=120), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", user_role, nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_index("ix_user_accounts_username", "user_accounts", ["username"])
    op.create_index("ix_user_accounts_role", "user_accounts", ["role"])


def downgrade() -> None:
    op.drop_index("ix_user_accounts_role", table_name="user_accounts")
    op.drop_index("ix_user_accounts_username", table_name="user_accounts")
    op.drop_table("user_accounts")
    sa.Enum(name="userrole").drop(op.get_bind(), checkfirst=True)
