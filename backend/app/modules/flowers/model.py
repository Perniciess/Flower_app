from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import DECIMAL, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Flower(Base):
    """Сущность цветка"""

    __tablename__ = "flower"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[Decimal | None] = mapped_column(DECIMAL(precision=10, scale=2))
    images: Mapped[list[FlowerImage]] = relationship(
        "FlowerImage", back_populates="flower", cascade="all, delete-orphan", order_by="FlowerImage.sort_order"
    )
    description: Mapped[str | None] = mapped_column(Text())
    color: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class FlowerImage(Base):
    """Сущность изображений цветка"""

    __tablename__ = "flower_image"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    flower_id: Mapped[int] = mapped_column(ForeignKey("flower.id", ondelete="CASCADE"))
    url: Mapped[str] = mapped_column(String(512))
    sort_order: Mapped[int] = mapped_column(index=True)

    flower: Mapped[Flower] = relationship("Flower", back_populates="images")
