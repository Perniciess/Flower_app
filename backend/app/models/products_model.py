from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import (
    DECIMAL,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.categories_model import product_category

if TYPE_CHECKING:
    from app.models.categories_model import Category


# Связующая таблица для состава букета (многие-ко-многим)
bouquet_composition = Table(
    "bouquet_composition",
    Base.metadata,
    Column(
        "product_id",
        Integer,
        ForeignKey("product.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "flower_id",
        Integer,
        ForeignKey("flower.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column("quantity", Integer, nullable=False, default=1),
)


class ProductType(StrEnum):
    FLOWER = "flower"
    GIFT = "gift"


class Product(Base):
    """Сущность товара."""

    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    type: Mapped[ProductType] = mapped_column(
        Enum(ProductType), default=ProductType.FLOWER, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[Decimal] = mapped_column(DECIMAL(precision=10, scale=2))
    sort_order: Mapped[int] = mapped_column(index=True)
    images: Mapped[list[ProductImage]] = relationship(
        "ProductImage",
        back_populates="product",
        cascade="all, delete-orphan",
        order_by="ProductImage.sort_order",
    )
    description: Mapped[str | None] = mapped_column(Text())
    color: Mapped[str | None] = mapped_column(String(64))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    in_stock: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    categories: Mapped[list[Category]] = relationship(
        "Category", secondary=product_category, back_populates="products"
    )
    composition: Mapped[list[Flower]] = relationship(
        "Flower", secondary=bouquet_composition, back_populates="products"
    )


class ProductImage(Base):
    """Сущность изображений цветка."""

    __tablename__ = "product_image"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("product.id", ondelete="CASCADE"), index=True
    )
    url: Mapped[str] = mapped_column(String(512))
    sort_order: Mapped[int] = mapped_column(index=True)

    product: Mapped[Product] = relationship("Product", back_populates="images")


class Flower(Base):
    """Сущность цветка."""

    __tablename__ = "flowers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    price: Mapped[Decimal] = mapped_column(DECIMAL(precision=10, scale=2))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
