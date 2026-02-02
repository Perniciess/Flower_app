from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from .products_model import Product
    from .users_model import User


class Favourite(Base):
    """Сущность понравившихся товаров."""

    __tablename__ = "favourite"
    __table_args__ = (
        UniqueConstraint("user_id", "product_id", name="uq_user_product"),
    )
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("product.id", ondelete="CASCADE"), index=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), index=True
    )

    product: Mapped["Product"] = relationship("Product")
    user: Mapped["User"] = relationship("User", back_populates="favourites")
