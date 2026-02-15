"""add image

Revision ID: 1c1ad97aac86
Revises: 1a91e4220608
Create Date: 2026-02-15 17:49:15.991540

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "1c1ad97aac86"
down_revision: Union[str, Sequence[str], None] = "1a91e4220608"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # --- advices (new table) ---
    op.create_table(
        "advices",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("image_url", sa.String(length=512), nullable=True),
        sa.Column("link", sa.String(length=512), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_advices_id"), "advices", ["id"], unique=False)
    op.create_index(op.f("ix_advices_is_active"), "advices", ["is_active"], unique=False)
    op.create_index(op.f("ix_advices_sort_order"), "advices", ["sort_order"], unique=False)
    op.create_index(op.f("ix_advices_title"), "advices", ["title"], unique=True)

    # --- flower -> flowers (rename to preserve data) ---
    op.drop_constraint(op.f("bouquet_composition_flower_id_fkey"), "bouquet_composition", type_="foreignkey")
    op.drop_index(op.f("ix_flower_id"), table_name="flower")
    op.rename_table("flower", "flowers")
    op.create_index(op.f("ix_flowers_id"), "flowers", ["id"], unique=False)
    op.create_foreign_key(None, "bouquet_composition", "flowers", ["flower_id"], ["id"], ondelete="CASCADE")

    # --- images (new table) ---
    op.create_table(
        "images",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("path", sa.String(), nullable=True),
        sa.Column("hash", sa.String(), nullable=True),
        sa.Column("original_filename", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("path"),
    )
    op.create_index(op.f("ix_images_hash"), "images", ["hash"], unique=False)
    op.create_index(op.f("ix_images_id"), "images", ["id"], unique=False)

    # --- product_image (new table, replaces product_image_link + old image) ---
    op.create_table(
        "product_image",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("url", sa.String(length=512), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["product_id"], ["product.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_product_image_id"), "product_image", ["id"], unique=False)
    op.create_index(op.f("ix_product_image_product_id"), "product_image", ["product_id"], unique=False)
    op.create_index(op.f("ix_product_image_sort_order"), "product_image", ["sort_order"], unique=False)

    # --- drop old tables (product_image_link depends on image, drop it first) ---
    op.drop_table("product_image_link")
    op.drop_index(op.f("ix_image_id"), table_name="image")
    op.drop_table("image")


def downgrade() -> None:
    """Downgrade schema."""
    op.create_table(
        "image",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("url", sa.VARCHAR(length=512), autoincrement=False, nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("image_pkey")),
    )
    op.create_index(op.f("ix_image_id"), "image", ["id"], unique=False)
    op.create_table(
        "product_image_link",
        sa.Column("product_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("image_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("sort_order", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["image_id"], ["image.id"], name=op.f("product_image_link_image_id_fkey"), ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["product_id"], ["product.id"], name=op.f("product_image_link_product_id_fkey"), ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("product_id", "image_id", name=op.f("product_image_link_pkey")),
    )

    op.drop_index(op.f("ix_product_image_sort_order"), table_name="product_image")
    op.drop_index(op.f("ix_product_image_product_id"), table_name="product_image")
    op.drop_index(op.f("ix_product_image_id"), table_name="product_image")
    op.drop_table("product_image")
    op.drop_index(op.f("ix_images_id"), table_name="images")
    op.drop_index(op.f("ix_images_hash"), table_name="images")
    op.drop_table("images")

    op.drop_constraint(None, "bouquet_composition", type_="foreignkey")
    op.drop_index(op.f("ix_flowers_id"), table_name="flowers")
    op.rename_table("flowers", "flower")
    op.create_index(op.f("ix_flower_id"), "flower", ["id"], unique=False)
    op.create_foreign_key(
        op.f("bouquet_composition_flower_id_fkey"),
        "bouquet_composition",
        "flower",
        ["flower_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.drop_index(op.f("ix_advices_title"), table_name="advices")
    op.drop_index(op.f("ix_advices_sort_order"), table_name="advices")
    op.drop_index(op.f("ix_advices_is_active"), table_name="advices")
    op.drop_index(op.f("ix_advices_id"), table_name="advices")
    op.drop_table("advices")
