from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CartItemBase(BaseModel):
    """Базовые поля товара в корзин, используемые в других схемах."""

    cart_id: int = Field(..., description="Уникальный идентификатор корзины")
    product_id: int = Field(..., description="Идентификатор товара")
    quantity: int = Field(..., description="Количество товара")
    price: Decimal = Field(..., description="Цена товара")


class CartItemCreate(BaseModel):
    """Схема для создания товара в корзине."""

    product_id: int = Field(..., description="Уникальный идентификатор товара")
    quantity: int = Field(default=1, ge=1, le=999)


class CartItemUpdate(BaseModel):
    """Схема для частичного обновления товара в корзине."""

    quantity: int | None = Field(default=None, ge=1, le=999, description="Количество товара")


class CartItemResponse(CartItemBase):
    """Схема ответа API ответа с информацией об товаре в корзине."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Уникальный идентификатор товара корзины")


class CartResponse(BaseModel):
    """Схема API ответа с информацией о корзине"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Уникальный идентификатор корзины")
    user_id: int = Field(..., description="Уникальный идентификатор пользователя")

    cart_item: list[CartItemResponse] = Field(default_factory=list, description="Товары в корзине")
