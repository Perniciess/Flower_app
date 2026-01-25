"""change email to phone

Revision ID: ea622af5101a
Revises: 27a28e81ca59
Create Date: 2026-01-24 04:56:06.766021
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "ea622af5101a"
down_revision: Union[str, Sequence[str], None] = "27a28e81ca59"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("user", sa.Column("phone_number", sa.String(length=12), nullable=True))
    op.drop_constraint(op.f("user_email_key"), "user", type_="unique")
    op.create_unique_constraint("user_phone_number_key", "user", ["phone_number"])
    op.drop_column("user", "email")


def downgrade() -> None:
    op.add_column("user", sa.Column("email", sa.VARCHAR(length=64), nullable=True))
    op.drop_constraint("user_phone_number_key", "user", type_="unique")
    op.create_unique_constraint(op.f("user_email_key"), "user", ["email"])
    op.drop_column("user", "phone_number")
