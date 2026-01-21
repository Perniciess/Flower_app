"""add defaults for flower timestamps

Revision ID: b454b869702d
Revises: 140fbfca087c
Create Date: 2026-01-21 03:56:35.322235

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b454b869702d'
down_revision: Union[str, Sequence[str], None] = '140fbfca087c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "flower",
        "created_at",
        server_default=sa.text("now()"),
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=False,
    )
    op.alter_column(
        "flower",
        "updated_at",
        server_default=sa.text("now()"),
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=False,
    )



def downgrade() -> None:
    """Downgrade schema."""
    pass
