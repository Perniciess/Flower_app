from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CartResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Уникальный идентификатор корзины")
    user_id: int = Field(..., description="Уникальный идентификатор пользователя")


class CartItemBase(BaseModel):
    cart_id: int = Field(..., description="Уникальный идентификатор корзины")
    quantity: int = Field(..., description="Количество товара")
    price: Decimal = Field(..., description="Цена товара")


class CartItemCreate(BaseModel):
    flower_id: int = Field(..., description="Уникальный идентификатор цветка")
    quantity: int = Field(default=1, ge=1)


class CartItemUpdate(BaseModel):
    quantity: int | None = Field(default=None, description="Количество товара")


class CartItemResponse(CartItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Уникальный идентификатор товара корзины")
