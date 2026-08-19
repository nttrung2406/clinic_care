"""create diagnosis_codes and consultations tables

Revision ID: 202608190001
Revises:
Create Date: 2026-08-19 00:01:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "202608190001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "diagnosis_codes",
        sa.Column("code", sa.String(length=10), primary_key=True),
        sa.Column("description", sa.Text(), nullable=False),
    )
    op.create_index(
        "ix_diagnosis_codes_description",
        "diagnosis_codes",
        ["description"],
    )

    op.create_table(
        "consultations",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("patient_name", sa.String(length=200), nullable=False),
        sa.Column("notes", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_consultations_patient_name", "consultations", ["patient_name"])

    op.create_table(
        "consultation_diagnosis_codes",
        sa.Column(
            "consultation_id",
            sa.Integer(),
            sa.ForeignKey("consultations.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "diagnosis_code",
            sa.String(length=10),
            sa.ForeignKey("diagnosis_codes.code", ondelete="RESTRICT"),
            primary_key=True,
        ),
    )


def downgrade() -> None:
    op.drop_table("consultation_diagnosis_codes")
    op.drop_index("ix_consultations_patient_name", table_name="consultations")
    op.drop_table("consultations")
    op.drop_index("ix_diagnosis_codes_description", table_name="diagnosis_codes")
    op.drop_table("diagnosis_codes")
