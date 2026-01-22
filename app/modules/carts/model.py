from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DECIMAL, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.modules.flowers.model import Flower


class Cart(Base):
    __tablename__ = "cart"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), unique=True)
    cart_item: Mapped[list[CartItem]] = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class CartItem(Base):
    __tablename__ = "cart_item"
    __table_args__ = (UniqueConstraint("cart_id", "flower_id", name="uq_cart_flower"), {})

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("cart.id", ondelete="CASCADE"))
    flower_id: Mapped[int] = mapped_column(ForeignKey("flower.id", ondelete="CASCADE"))
    quantity: Mapped[int] = mapped_column()
    price: Mapped[Decimal] = mapped_column(DECIMAL(precision=10, scale=2))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    cart: Mapped[Cart] = relationship("Cart", back_populates="cart_item")
    flower: Mapped[Flower] = relationship("Flower")
