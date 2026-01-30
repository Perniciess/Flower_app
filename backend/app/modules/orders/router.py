import uuid
from collections.abc import Sequence
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.deps import require_client
from app.database.session import get_db
from app.modules.users.model import User

from . import service as order_service
from .schema import OrderResponse, OrderResponseWithPayment, WebhookPayload

order_router = APIRouter(prefix="/orders", tags=["orders"])


@order_router.post(
    "/create", summary="Создание заказа", response_model=OrderResponseWithPayment
)
async def create_order(
    user: User = Depends(require_client), session: AsyncSession = Depends(get_db)
) -> OrderResponseWithPayment:
    return await order_service.create_order(
        session=session,
        user_id=user.id,
        idempotency_key=uuid.uuid4(),
        expires_at=datetime.now(UTC)
        + timedelta(minutes=settings.ORDER_EXPIRATION_MINUTES),
    )


@order_router.post("/webhook", summary="Webhook YooKassa")
async def yookassa_webhook(
    payload: WebhookPayload, session: AsyncSession = Depends(get_db)
) -> None:
    await order_service.process_webhook(session=session, payload=payload)


@order_router.get(
    "history",
    response_model=Sequence[OrderResponse],
    summary="История заказов пользователя",
)
async def get_orders(
    current_user: User = Depends(require_client),
    session: AsyncSession = Depends(get_db),
) -> Sequence[OrderResponse]:
    orders = await order_service.get_orders(session=session, user_id=current_user.id)
    return orders


@order_router.get(
    "/{order_id}", response_model=OrderResponse, summary="Получить информацию о заказе"
)
async def get_order_by_id(
    order_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_client),
) -> OrderResponse:
    order = await order_service.get_order_by_id(session=session, order_id=order_id)
    return order
