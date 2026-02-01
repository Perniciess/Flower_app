from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import DECIMAL, Boolean, CheckConstraint, DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from .categories_model import Category
    from .products_model import Product


class DiscountType(StrEnum):
    PRODUCT = "product"
    CATEGORY = "category"


class Discount(Base):
    """Сущность акции."""

    __tablename__ = "discount"
    __table_args__ = (
        CheckConstraint(
            "(product_id IS NOT NULL) != (category_id IS NOT NULL)",
            name="ck_discount_one_target",
        ),
        CheckConstraint(
            "(percentage IS NOT NULL) != (new_price IS NOT NULL)",
            name="ck_discount_one_value",
        ),
        CheckConstraint(
            "category_id IS NULL OR new_price IS NULL",
            name="ck_category_no_new_price",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    discount_type: Mapped[DiscountType] = mapped_column(Enum(DiscountType))
    percentage: Mapped[Decimal | None] = mapped_column(DECIMAL(precision=5, scale=2))
    new_price: Mapped[Decimal | None] = mapped_column(DECIMAL(precision=10, scale=2))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    product_id: Mapped[int | None] = mapped_column(ForeignKey("product.id", ondelete="CASCADE"), index=True)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("category.id", ondelete="CASCADE"), index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    product: Mapped[Product | None] = relationship("Product", backref="discounts")
    category: Mapped[Category | None] = relationship("Category", backref="discounts")
