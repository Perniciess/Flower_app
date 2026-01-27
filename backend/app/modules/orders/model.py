from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import DECIMAL, DateTime, Enum, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.modules.flowers.model import Flower


class Status(StrEnum):
    PENDING = "pending"
    PAID = "pad"
    IN_PROGRESS = "in_progress"
    DELIVERED = "delivered"
    ON_THE_WAY = "on_the_way"
    CANCELLED = "cancelled"


class Order(Base):
    """Сущность заказа."""

    __tablename__ = "order"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), unique=True)
    status: Mapped[Status] = mapped_column(Enum(Status), default=Status.PENDING)
    total_price: Mapped[Decimal] = mapped_column(DECIMAL(precision=10, scale=2))

    # payment ??

    order_item: Mapped[list[OrderItem]] = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class OrderItem(Base):
    """Сущность товара в заказе."""

    __tablename__ = "order_item"
    __table_args__ = (UniqueConstraint("order_id", "flower_id", name="uq_order_flower"), {})

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("order.id", ondelete="CASCADE"))
    flower_id: Mapped[int] = mapped_column(ForeignKey("flower.id", ondelete="CASCADE"))
    quantity: Mapped[int] = mapped_column()
    price: Mapped[Decimal] = mapped_column(DECIMAL(precision=10, scale=2))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    order: Mapped[Order] = relationship("Order", back_populates="order_item")
    flower: Mapped[Flower] = relationship("Flower")
