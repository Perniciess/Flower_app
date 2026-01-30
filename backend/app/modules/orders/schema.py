from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)
from pydantic_extra_types.phone_numbers import PhoneNumber

from app.core.utils import normalize_phone

from .model import MethodOfReceipt


class OrderItemBase(BaseModel):
    """Базовые поля товара в закзаа, используемые в других схемах."""

    order_id: int = Field(..., description="Уникальный идентификатор заказа")
    product_id: int = Field(..., description="Идентификатор товара")
    quantity: int = Field(..., description="Количество товара")
    price: Decimal = Field(..., description="Цена товара")


class OrderItemResponse(OrderItemBase):
    """Схема ответа API овтета товара в заказе."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Уникальный идентификатор товара заказа")


class DeliveryResponse(BaseModel):
    """Схема API ответа доставки"""

    model_config = ConfigDict(from_attributes=True)

    address: str = Field(..., description="Адрес доставки")
    recipient_name: str | None = Field(None, description="Имя получателя")
    recipient_phone: str | None = Field(None, description="Телефон получателя")
    comment: str | None = Field(None, description="Комментарий")


class OrderResponse(BaseModel):
    """Схема API ответа заказа"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Уникальный идентификатор заказа")
    user_id: int = Field(..., description="Уникальный идентификатор пользователя")
    method_of_receipt: MethodOfReceipt = Field(..., description="Метод получения")
    delivery: DeliveryResponse | None = Field(None, description="Данные доставки")

    order_item: list[OrderItemResponse] = Field(default_factory=list, description="Товары в заказе")


class OrderResponseWithPayment(OrderResponse):
    payment_id: str = Field(..., description="Уникальный идентификатор оплаты")
    confirmation_url: str = Field(..., description="Ссылка на оплату")


class WebhookPaymentObject(BaseModel):
    id: str = Field(..., description="Уникальный идентификатор хука оплаты")
    status: str = Field(..., description="Статус оплаты")


class WebhookPayload(BaseModel):
    event: str = Field(...)
    object: WebhookPaymentObject = Field(...)


class CreateOrderRequest(BaseModel):
    method: MethodOfReceipt = Field(..., description="Метод получения")
    address: str | None = Field(default=None, description="Адрес доставки")
    recipient_name: str | None = Field(default=None, description="Имя получателя")
    recipient_phone: PhoneNumber = Field(..., description="Номер телефона получателя")
    comment: str | None = Field(default=None, description="Комментарий к заказу")

    @model_validator(mode="after")
    def check_address(self):
        if self.method == MethodOfReceipt.DELIVERY and not self.address:
            raise ValueError("Для доставки необходим адрес")
        return self

    @field_validator("recipient_phone")
    @classmethod
    def normalize_phone(cls, v: PhoneNumber) -> str:
        return normalize_phone(v)
