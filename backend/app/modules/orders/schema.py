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


class OrderItemResponse(BaseModel):
    """Схема API ответа товара в заказе."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Уникальный идентификатор товара заказа")
    order_id: int = Field(..., description="Уникальный идентификатор заказа")
    product_id: int = Field(..., description="Идентификатор товара")
    quantity: int = Field(..., description="Количество товара")
    price: Decimal = Field(..., description="Цена товара")


class DeliveryResponse(BaseModel):
    """Схема API ответа доставки."""

    model_config = ConfigDict(from_attributes=True)

    address: str = Field(..., description="Адрес доставки")
    recipient_name: str | None = Field(None, description="Имя получателя")
    recipient_phone: str | None = Field(None, description="Телефон получателя")
    comment: str | None = Field(None, description="Комментарий")


class DeliveryRequest(BaseModel):
    """Схема доставки в запросе на создание заказа."""

    address: str = Field(..., description="Адрес доставки")
    recipient_name: str | None = Field(None, description="Имя получателя")
    recipient_phone: PhoneNumber = Field(..., description="Телефон получателя")
    comment: str | None = Field(None, description="Комментарий")

    @field_validator("recipient_phone")
    @classmethod
    def normalize_phone(cls, v: PhoneNumber) -> str:
        return normalize_phone(v)


class OrderResponse(BaseModel):
    """Схема API ответа заказа."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Уникальный идентификатор заказа")
    user_id: int = Field(..., description="Уникальный идентификатор пользователя")
    method_of_receipt: MethodOfReceipt = Field(..., description="Метод получения")
    delivery: DeliveryResponse | None = Field(None, description="Данные доставки")
    pickup_point_id: int | None = Field(None, description="Идентификатор точки самовывоза")
    order_item: list[OrderItemResponse] = Field(default_factory=list, description="Товары в заказе")


class OrderResponseWithPayment(OrderResponse):
    """Схема API ответа с ссылкой на оплату."""

    payment_id: str = Field(..., description="Уникальный идентификатор оплаты")
    confirmation_url: str = Field(..., description="Ссылка на оплату")


class WebhookPaymentObject(BaseModel):
    """Объект оплаты в webhook-уведомлении ЮKassa."""

    id: str = Field(..., description="Уникальный идентификатор хука оплаты")
    status: str = Field(..., description="Статус оплаты")


class WebhookPayload(BaseModel):
    """Схема webhook-уведомления ЮKassa."""

    event: str = Field(...)
    object: WebhookPaymentObject = Field(...)


class CreateOrderRequest(BaseModel):
    """Схема для создания заказа."""

    method_of_receipt: MethodOfReceipt = Field(..., description="Метод получения")
    delivery: DeliveryRequest | None = Field(default=None, description="Данные доставки")
    pickup_point_id: int | None = Field(default=None, description="Идентификатор точки самовывоза")

    @model_validator(mode="after")
    def check_delivery(self):
        if self.method_of_receipt == MethodOfReceipt.DELIVERY:
            if not self.delivery:
                raise ValueError("Для доставки необходимы данные доставки")
            if self.pickup_point_id is not None:
                raise ValueError("Для доставки не требуется точка самовывоза")

        if self.method_of_receipt == MethodOfReceipt.PICK_UP:
            if self.delivery is not None:
                raise ValueError("Для самовывоза не нужны данные доставки")
            if not self.pickup_point_id:
                raise ValueError("Для самовывоза необходимо выбрать точку самовывоза")

        return self
