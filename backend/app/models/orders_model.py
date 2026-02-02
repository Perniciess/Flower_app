from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import (
    DECIMAL,
    DateTime,
    Enum,
    ForeignKey,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from .pickups_model import PickupPoint
    from .products_model import Product


class Status(StrEnum):
    PENDING = "pending"
    PAID = "paid"
    IN_PROGRESS = "in_progress"
    DELIVERED = "delivered"
    ON_THE_WAY = "on_the_way"
    CANCELLED = "cancelled"


class MethodOfReceipt(StrEnum):
    DELIVERY = "delivery"
    PICK_UP = "pick_up"


class Order(Base):
    """Сущность заказа."""

    __tablename__ = "order"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), index=True
    )
    status: Mapped[Status] = mapped_column(Enum(Status), default=Status.PENDING)
    total_price: Mapped[Decimal] = mapped_column(DECIMAL(precision=10, scale=2))
    method_of_receipt: Mapped[MethodOfReceipt] = mapped_column(Enum(MethodOfReceipt))
    payment_id: Mapped[str | None] = mapped_column(index=True, unique=True)
    idempotency_key: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        unique=True,
        nullable=False,
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    paid_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    pickup_point_id: Mapped[int | None] = mapped_column(
        ForeignKey("pickup_point.id", ondelete="SET NULL"), nullable=True
    )

    order_item: Mapped[list[OrderItem]] = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )
    delivery: Mapped[Delivery | None] = relationship(
        "Delivery", back_populates="order", uselist=False, cascade="all, delete-orphan"
    )
    pickup_point: Mapped[PickupPoint | None] = relationship("PickupPoint")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class OrderItem(Base):
    """Сущность товара в заказе."""

    __tablename__ = "order_item"
    __table_args__ = (
        UniqueConstraint("order_id", "product_id", name="uq_order_product"),
        {},
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("order.id", ondelete="CASCADE"), index=True
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("product.id", ondelete="CASCADE"), index=True
    )
    quantity: Mapped[int] = mapped_column()
    price: Mapped[Decimal] = mapped_column(DECIMAL(precision=10, scale=2))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    order: Mapped[Order] = relationship("Order", back_populates="order_item")
    product: Mapped[Product] = relationship("Product")


class Delivery(Base):
    __tablename__ = "delivery"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("order.id", ondelete="CASCADE"), unique=True, index=True
    )
    address: Mapped[str] = mapped_column(String(512))
    recipient_name: Mapped[str | None] = mapped_column(String(128))
    recipient_phone: Mapped[str | None] = mapped_column(String(16))
    comment: Mapped[str | None] = mapped_column(String(512))
    delivery_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    order: Mapped[Order] = relationship("Order", back_populates="delivery")
