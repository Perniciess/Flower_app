from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "ff5f73bb2058"
down_revision: Union[str, Sequence[str], None] = "ea622af5101a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "user",
        "phone_number",
        existing_type=sa.VARCHAR(length=12),
        type_=sa.String(length=16),
        existing_nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "user",
        "phone_number",
        existing_type=sa.String(length=16),
        type_=sa.VARCHAR(length=12),
        existing_nullable=True,
    )
