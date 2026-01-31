import uuid
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.deps import require_admin, require_client
from app.database.session import get_db
from app.modules.users.model import User

from . import service as order_service
from .model import Status
from .schema import (
    CreateOrderRequest,
    OrderResponse,
    OrderResponseWithPayment,
    WebhookPayload,
)

order_router = APIRouter(prefix="/orders", tags=["orders"])


@order_router.post("/create", summary="Создание заказа", response_model=OrderResponseWithPayment)
async def create_order(
    data: CreateOrderRequest,
    user: User = Depends(require_client),
    session: AsyncSession = Depends(get_db),
) -> OrderResponseWithPayment:
    """
    Создать заказ.

    Требует авторизации.
    """
    return await order_service.create_order(
        session=session,
        user_id=user.id,
        data=data,
        idempotency_key=uuid.uuid4(),
        expires_at=datetime.now(UTC) + timedelta(minutes=settings.ORDER_EXPIRATION_MINUTES),
    )


@order_router.post("/webhook", summary="Webhook YooKassa")
async def yookassa_webhook(payload: WebhookPayload, session: AsyncSession = Depends(get_db)) -> None:
    """
    Получить ответ от юkassa со статусом оплаты.
    """
    await order_service.process_webhook(session=session, payload=payload)


@order_router.get(
    "/history",
    response_model=Page[OrderResponse],
    summary="История заказов пользователя",
)
async def get_orders(
    current_user: User = Depends(require_client),
    session: AsyncSession = Depends(get_db),
) -> Page[OrderResponse]:
    """
    Получить список заказов.

    Требует авторизации.
    """
    orders = await order_service.get_orders(session=session, user_id=current_user.id)
    return orders


@order_router.get(
    "/{order_id:int}",
    response_model=OrderResponse,
    summary="Получить информацию о заказе",
)
async def get_order_by_id(
    order_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_client),
) -> OrderResponse:
    """
    Получить информацию о заказе.

    Требует авторизации.
    """
    order = await order_service.get_order_by_id(session=session, order_id=order_id)
    return order


@order_router.patch(
    "/status/{order_id:int}",
    response_model=OrderResponse,
    summary="Обновить статус заказа",
)
async def update_order_status(
    order_id: int,
    status: Status,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_client),
) -> OrderResponse:
    """
    Обновить статус заказа.

    Требует авторизации.
    """
    order = await order_service.update_order_status(session=session, order_id=order_id, status=status)
    return order


@order_router.get(
    "/paid",
    response_model=Page[OrderResponse],
    summary="Получить все оплаченные заказы",
)
async def get_all_paid_orders(session: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)):
    """
    Получить список оплаченныз заказов.

    Требует прав администратора.
    """
    orders = await order_service.get_all_paid_orders(session=session)
    return orders


@order_router.get("/all", response_model=Page[OrderResponse], summary="Получить все заказы")
async def get_all_orders(session: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)):
    """
    Получить список всех заказов.

    Требует прав администратора.
    """
    orders = await order_service.get_all_orders(session=session)
    return orders
