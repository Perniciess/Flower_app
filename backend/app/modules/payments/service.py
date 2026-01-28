import base64
import uuid
from decimal import Decimal

import httpx

from app.core.config import settings


async def create_yookassa_payment(
    *,
    amount: Decimal,
    order_id: int,
    idempotency_key: uuid.UUID,
) -> tuple[str, str]:
    auth = base64.b64encode(f"{settings.YOOKASSA_SHOP_ID}:{settings.YOOKASSA_SECRET_KEY}".encode()).decode()

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.yookassa.ru/v3/payments",
            headers={
                "Authorization": f"Basic {auth}",
                "Idempotence-Key": str(idempotency_key),
                "Content-Type": "application/json",
            },
            json={
                "amount": {"value": amount, "currency": "RUB"},
                "confirmation": {
                    "type": "redirect",
                    "return_url": settings.PAYMENT_RETURN_URL,
                },
                "capture": True,
                "description": f"Заказ #{order_id}",
                "metadata": {"order_id": order_id},
            },
        )
        response.raise_for_status()
        data = response.json()

    return data["id"], data["confirmation"]["confirmation_url"]
