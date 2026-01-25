"""add default for refresh_token.created_at

Revision ID: 84e194f3104e
Revises: b454b869702d
Create Date: 2026-01-22 00:27:10.930478

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84e194f3104e'
down_revision: Union[str, Sequence[str], None] = 'b454b869702d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        "refresh_token",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        nullable=False,
        server_default=sa.text("now()"),
    )

def downgrade():
    op.alter_column(
        "refresh_token",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        nullable=False,
        server_default=None,
    )
