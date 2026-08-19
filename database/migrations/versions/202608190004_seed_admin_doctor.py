"""seed default admin doctor account

Revision ID: 202608190004
Revises: 202608190003
Create Date: 2026-08-19 00:04:00

"""
import os
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "202608190004"
down_revision: Union[str, None] = "202608190003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

doctors_table = sa.table(
    "doctors",
    sa.column("username", sa.String),
    sa.column("password_hash", sa.String),
)


def _admin_username() -> str:
    return os.environ.get("ADMIN_USERNAME")


def _admin_password_hash() -> str:
    return os.environ.get("ADMIN_PASSWORD_HASH")


def upgrade() -> None:
    op.bulk_insert(
        doctors_table,
        [{"username": _admin_username(), "password_hash": _admin_password_hash()}],
    )


def downgrade() -> None:
    op.execute(doctors_table.delete().where(doctors_table.c.username == _admin_username()))
