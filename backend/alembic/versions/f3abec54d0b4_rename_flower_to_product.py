"""rename flower to product

Revision ID: f3abec54d0b4
Revises: 27bd76c8910d
Create Date: 2026-01-30 23:13:20.793165

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "f3abec54d0b4"
down_revision: Union[str, Sequence[str], None] = "27bd76c8910d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Rename tables
    op.rename_table("flower", "product")
    op.rename_table("flower_image", "product_image")

    # Rename indexes on product
    op.execute("ALTER INDEX ix_flower_id RENAME TO ix_product_id")

    # Rename indexes on product_image
    op.execute("ALTER INDEX ix_flower_image_id RENAME TO ix_product_image_id")
    op.execute("ALTER INDEX ix_flower_image_sort_order RENAME TO ix_product_image_sort_order")

    # Rename FK column and constraint in product_image
    op.alter_column("product_image", "flower_id", new_column_name="product_id")
    op.execute("ALTER TABLE product_image RENAME CONSTRAINT flower_image_flower_id_fkey TO product_image_product_id_fkey")

    # Rename FK column and constraint in cart_item
    op.alter_column("cart_item", "flower_id", new_column_name="product_id")
    op.execute("ALTER TABLE cart_item RENAME CONSTRAINT cart_item_flower_id_fkey TO cart_item_product_id_fkey")
    op.drop_constraint("uq_cart_flower", "cart_item", type_="unique")
    op.create_unique_constraint("uq_cart_product", "cart_item", ["cart_id", "product_id"])

    # Rename FK column and constraint in order_item
    op.alter_column("order_item", "flower_id", new_column_name="product_id")
    op.execute("ALTER TABLE order_item RENAME CONSTRAINT order_item_flower_id_fkey TO order_item_product_id_fkey")
    op.drop_constraint("uq_order_flower", "order_item", type_="unique")
    op.create_unique_constraint("uq_order_product", "order_item", ["order_id", "product_id"])

    # Rename PK constraints
    op.execute("ALTER TABLE product RENAME CONSTRAINT flower_pkey TO product_pkey")
    op.execute("ALTER TABLE product_image RENAME CONSTRAINT flower_image_pkey TO product_image_pkey")

    # Add delivery table and method_of_receipt (new additions in this migration)
    methodofreceipt = sa.Enum("DELIVERY", "PICK_UP", name="methodofreceipt")
    methodofreceipt.create(op.get_bind())
    op.add_column("order", sa.Column("method_of_receipt", methodofreceipt, nullable=True))
    op.execute("UPDATE \"order\" SET method_of_receipt = 'PICK_UP' WHERE method_of_receipt IS NULL")
    op.alter_column("order", "method_of_receipt", nullable=False)
    op.create_table(
        "delivery",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("address", sa.String(length=512), nullable=False),
        sa.Column("recipient_name", sa.String(length=128), nullable=True),
        sa.Column("recipient_phone", sa.String(length=16), nullable=True),
        sa.Column("comment", sa.String(length=512), nullable=True),
        sa.Column("delivery_date", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["order_id"], ["order.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("order_id"),
    )
    op.create_index(op.f("ix_delivery_id"), "delivery", ["id"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Drop delivery
    op.drop_index(op.f("ix_delivery_id"), table_name="delivery")
    op.drop_table("delivery")
    op.drop_column("order", "method_of_receipt")
    op.execute("DROP TYPE IF EXISTS methodofreceipt")

    # Revert order_item
    op.drop_constraint("uq_order_product", "order_item", type_="unique")
    op.create_unique_constraint("uq_order_flower", "order_item", ["order_id", "flower_id"])
    op.execute("ALTER TABLE order_item RENAME CONSTRAINT order_item_product_id_fkey TO order_item_flower_id_fkey")
    op.alter_column("order_item", "product_id", new_column_name="flower_id")

    # Revert cart_item
    op.drop_constraint("uq_cart_product", "cart_item", type_="unique")
    op.create_unique_constraint("uq_cart_flower", "cart_item", ["cart_id", "flower_id"])
    op.execute("ALTER TABLE cart_item RENAME CONSTRAINT cart_item_product_id_fkey TO cart_item_flower_id_fkey")
    op.alter_column("cart_item", "product_id", new_column_name="flower_id")

    # Revert product_image
    op.execute("ALTER TABLE product_image RENAME CONSTRAINT product_image_product_id_fkey TO flower_image_flower_id_fkey")
    op.alter_column("product_image", "product_id", new_column_name="flower_id")

    # Revert PK constraints
    op.execute("ALTER TABLE product RENAME CONSTRAINT product_pkey TO flower_pkey")
    op.execute("ALTER TABLE product_image RENAME CONSTRAINT product_image_pkey TO flower_image_pkey")

    # Revert indexes
    op.execute("ALTER INDEX ix_product_image_sort_order RENAME TO ix_flower_image_sort_order")
    op.execute("ALTER INDEX ix_product_image_id RENAME TO ix_flower_image_id")
    op.execute("ALTER INDEX ix_product_id RENAME TO ix_flower_id")

    # Revert table names
    op.rename_table("product_image", "flower_image")
    op.rename_table("product", "flower")
