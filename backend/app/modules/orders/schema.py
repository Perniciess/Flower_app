from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class OrderItemBase(BaseModel):
    """Базовые поля товара в закзаа, используемые в других схемах."""

    order_id: int = Field(..., description="Уникальный идентификатор заказа")
    flower_id: int = Field(..., description="Идентификатор цветка")
    quantity: int = Field(..., description="Количество товара")
    price: Decimal = Field(..., description="Цена товара")


class OrderItemResponse(OrderItemBase):
    """Схема ответа API овтета товара в заказе."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Уникальный идентификатор товара заказа")


class OrderResponse(BaseModel):
    """Схема API ответа заказа"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Уникальный идентификатор корзины")
    user_id: int = Field(..., description="Уникальный идентификатор пользователя")

    cart_item: list[OrderItemResponse] = Field(default_factory=list, description="Товары в корзине")
