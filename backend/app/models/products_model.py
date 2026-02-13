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


# Связующая таблица для изображений товара (многие-ко-многим)
product_image_link = Table(
    "product_image_link",
    Base.metadata,
    Column(
        "product_id",
        Integer,
        ForeignKey("product.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "image_id",
        Integer,
        ForeignKey("image.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column("sort_order", Integer, nullable=False, default=0),
)


class ProductType(StrEnum):
    FLOWER = "flower"
    GIFT = "gift"


class Product(Base):
    """Сущность товара."""

    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    type: Mapped[ProductType] = mapped_column(Enum(ProductType), default=ProductType.FLOWER, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[Decimal] = mapped_column(DECIMAL(precision=10, scale=2))
    sort_order: Mapped[int] = mapped_column(index=True)
    images: Mapped[list[Image]] = relationship(
        "Image",
        secondary=product_image_link,
        back_populates="products",
        order_by=product_image_link.c.sort_order,
    )
    description: Mapped[str | None] = mapped_column(Text())
    color: Mapped[str | None] = mapped_column(String(64))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    in_stock: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    categories: Mapped[list[Category]] = relationship("Category", secondary=product_category, back_populates="products")
    composition: Mapped[list[Flower]] = relationship("Flower", secondary=bouquet_composition, back_populates="products")


class Image(Base):
    """Сущность изображения."""

    __tablename__ = "image"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    url: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    products: Mapped[list[Product]] = relationship("Product", secondary=product_image_link, back_populates="images")


class Flower(Base):
    """Сущность цветка-ингредиента для состава букета."""

    __tablename__ = "flower"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    price: Mapped[Decimal] = mapped_column(DECIMAL(precision=10, scale=2))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    products: Mapped[list[Product]] = relationship(
        "Product", secondary=bouquet_composition, back_populates="composition"
    )
