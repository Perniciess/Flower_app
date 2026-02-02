import uuid
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, Request, status
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.deps import require_admin, require_client, verify_yookassa_request
from app.core.limiter import limiter
from app.db.session import get_db
from app.models.orders_model import Status
from app.models.users_model import User
from app.schemas.orders_schema import (
    CreateOrderRequest,
    OrderResponse,
    OrderResponseWithPayment,
    WebhookPayload,
)
from app.service import orders_service

order_router = APIRouter(prefix="/orders", tags=["orders"])


@order_router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    summary="Создание заказа",
    response_model=OrderResponseWithPayment,
)
@limiter.limit("10/minute")
async def create_order(
    request: Request,
    data: CreateOrderRequest,
    user: User = Depends(require_client),
    session: AsyncSession = Depends(get_db),
) -> OrderResponseWithPayment:
    """
    Создать заказ.

    Требует авторизации.
    """
    return await orders_service.create_order(
        session=session,
        user_id=user.id,
        data=data,
        idempotency_key=uuid.uuid4(),
        expires_at=datetime.now(UTC)
        + timedelta(minutes=settings.ORDER_EXPIRATION_MINUTES),
    )


@order_router.post(
    "/webhook", status_code=status.HTTP_204_NO_CONTENT, summary="Webhook YooKassa"
)
@limiter.limit("100/minute")
async def yookassa_webhook(
    request: Request,
    payload: WebhookPayload,
    session: AsyncSession = Depends(get_db),
    security: None = Depends(verify_yookassa_request),
) -> None:
    """
    Получить ответ от юkassa со статусом оплаты.
    """
    await orders_service.process_webhook(session=session, payload=payload)


@order_router.get(
    "/history",
    response_model=Page[OrderResponse],
    status_code=status.HTTP_200_OK,
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
    orders = await orders_service.get_orders(session=session, user_id=current_user.id)
    return orders


@order_router.get(
    "/{order_id}",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
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
    order = await orders_service.get_order_by_id(
        session=session, order_id=order_id, current_user=current_user
    )
    return order


@order_router.patch(
    "/status/{order_id}",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
    summary="Обновить статус заказа",
)
async def update_order_status(
    order_id: int,
    status: Status,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> OrderResponse:
    """
    Обновить статус заказа.

    Требует прав администратора.
    """
    order = await orders_service.update_order_status(
        session=session, order_id=order_id, status=status
    )
    return order


@order_router.patch(
    "/{order_id}/cancel",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
    summary="Отменить заказ",
)
async def cancel_order(
    order_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_client),
) -> OrderResponse:
    """
    Отменить заказ.

    Требует авторизации.
    """
    order = await orders_service.cancel_order(
        session=session, order_id=order_id, user_id=current_user.id
    )
    return order


@order_router.get(
    "/paid",
    response_model=Page[OrderResponse],
    status_code=status.HTTP_200_OK,
    summary="Получить все оплаченные заказы",
)
async def get_all_paid_orders(
    session: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)
):
    """
    Получить список оплаченных заказов.

    Требует прав администратора.
    """
    orders = await orders_service.get_all_paid_orders(session=session)
    return orders


@order_router.get(
    "/all",
    response_model=Page[OrderResponse],
    status_code=status.HTTP_200_OK,
    summary="Получить все заказы",
)
async def get_all_orders(
    session: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)
):
    """
    Получить список всех заказов.

    Требует прав администратора.
    """
    orders = await orders_service.get_all_orders(session=session)
    return orders
