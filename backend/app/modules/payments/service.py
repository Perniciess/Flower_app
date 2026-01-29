import uuid
from decimal import Decimal

from yookassa import Configuration, Payment

from app.core.config import settings
from app.core.exceptions import PaymentCreationError

Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


def create_yookassa_payment(
    *,
    amount: Decimal,
    order_id: int,
    idempotency_key: uuid.UUID,
) -> tuple[str, str]:
    payment = Payment.create(
        {
            "amount": {"value": f"{amount:.2f}", "currency": "RUB"},
            "confirmation": {
                "type": "redirect",
                "return_url": settings.PAYMENT_RETURN_URL,
            },
            "capture": settings.CAPTURE,
            "description": f"Заказ #{order_id}",
            "metadata": {"order_id": order_id},
        },
        idempotency_key,
    )

    if payment.id is None or payment.confirmation is None:
        raise PaymentCreationError(order_id=order_id)

    return payment.id, payment.confirmation.confirmation_url


def find_yookassa_payment(payment_id: str) -> tuple[str, str | None]:
    """Возвращает (status, confirmation_url | None) для существующего платежа."""
    payment = Payment.find_one(payment_id)
    confirmation_url: str | None = None
    if payment.confirmation is not None:
        confirmation_url = str(payment.confirmation.confirmation_url)
    return str(payment.status), confirmation_url
