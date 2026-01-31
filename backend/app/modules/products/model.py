from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import DECIMAL, DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.modules.categories.model import product_category

if TYPE_CHECKING:
    from app.modules.categories.model import Category


class ProductType(StrEnum):
    FLOWER = "flower"
    GIFT = "gift"


class Product(Base):
    """Сущность товара."""

    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    type: Mapped[ProductType] = mapped_column(
        Enum(ProductType), default=ProductType.FLOWER
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[Decimal] = mapped_column(DECIMAL(precision=10, scale=2))
    images: Mapped[list[ProductImage]] = relationship(
        "ProductImage",
        back_populates="product",
        cascade="all, delete-orphan",
        order_by="ProductImage.sort_order",
    )
    description: Mapped[str | None] = mapped_column(Text())
    color: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    categories: Mapped[list[Category]] = relationship(
        "Category", secondary=product_category, back_populates="products"
    )


class ProductImage(Base):
    """Сущность изображений цветка."""

    __tablename__ = "product_image"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("product.id", ondelete="CASCADE")
    )
    url: Mapped[str] = mapped_column(String(512))
    sort_order: Mapped[int] = mapped_column(index=True)

    product: Mapped[Product] = relationship("Product", back_populates="images")
