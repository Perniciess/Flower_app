import uuid
from datetime import UTC, datetime

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    CartNotFoundError,
    EmptyCartError,
    OrderNotFoundError,
    OrderNotUpdatedError,
)
from app.modules.carts import repository as cart_repository
from app.modules.payments import service as payment_service

from . import repository as order_repository
from .model import Order, Status
from .schema import (
    CreateOrderRequest,
    OrderResponse,
    OrderResponseWithPayment,
    WebhookPayload,
)


async def create_order(
    *,
    session: AsyncSession,
    data: CreateOrderRequest,
    user_id: int,
    idempotency_key: uuid.UUID,
    expires_at: datetime,
) -> OrderResponseWithPayment:
    cart = await cart_repository.get_cart_by_user_id(session=session, user_id=user_id)
    if cart is None:
        raise CartNotFoundError(user_id=user_id)

    if not cart.cart_item:
        raise EmptyCartError(cart_id=cart.id)

    pending_order = await order_repository.get_pending_order_by_user_id(session=session, user_id=user_id)
    if pending_order is not None:
        if pending_order.expires_at > datetime.now(UTC) and pending_order.payment_id is not None:
            payment_status, confirmation_url = payment_service.find_yookassa_payment(pending_order.payment_id)
            if payment_status == "pending" and confirmation_url is not None:
                return _build_response_with_payment(pending_order, pending_order.payment_id, confirmation_url)

        await order_repository.update_order_status(session=session, order_id=pending_order.id, status=Status.CANCELLED)

    order = await order_repository.create_order(
        session=session,
        user_id=user_id,
        data=data,
        cart=cart,
        idempotency_key=idempotency_key,
        expires_at=expires_at,
    )
    payment_id, confirmation_url = payment_service.create_yookassa_payment(
        amount=order.total_price, order_id=order.id, idempotency_key=idempotency_key
    )
    await order_repository.update_payment_id(session=session, order_id=order.id, payment_id=payment_id)

    return _build_response_with_payment(order, payment_id, confirmation_url)


async def process_webhook(*, session: AsyncSession, payload: WebhookPayload) -> None:
    order = await order_repository.get_order_by_payment_id(session=session, payment_id=payload.object.id)
    if order is None:
        return

    if payload.event == "payment.succeeded":
        await order_repository.mark_order_paid(session=session, order_id=order.id)
        cart = await cart_repository.get_cart_by_user_id(session=session, user_id=order.user_id)
        if cart is not None:
            await cart_repository.clear_cart(session=session, cart_id=cart.id)
    elif payload.event == "payment.canceled":
        await order_repository.update_order_status(session=session, order_id=order.id, status=Status.CANCELLED)


async def get_orders(session: AsyncSession, user_id: int) -> Page[OrderResponse]:
    query = order_repository.get_orders_query(user_id=user_id)
    return await paginate(session, query)


async def get_order_by_id(session: AsyncSession, order_id: int) -> OrderResponse:
    order = await order_repository.get_order_by_id(session=session, order_id=order_id)
    if order is None:
        raise OrderNotFoundError(order_id=order_id)

    return OrderResponse.model_validate(order)


async def update_order_status(session: AsyncSession, order_id: int, status: Status) -> OrderResponse:
    order = await order_repository.get_order_by_id(session=session, order_id=order_id)
    if order is None:
        raise OrderNotFoundError(order_id=order_id)
    updated = await order_repository.update_order_status(session=session, order_id=order_id, status=status)
    if updated is None:
        raise OrderNotUpdatedError(order_id=order_id)

    return OrderResponse.model_validate(updated)


async def get_all_orders(session: AsyncSession) -> Page[OrderResponse]:
    query = order_repository.get_all_orders_query()
    return await paginate(session, query)


async def get_all_paid_orders(session: AsyncSession) -> Page[OrderResponse]:
    query = order_repository.get_all_paid_query()
    return await paginate(session, query)


def _build_response_with_payment(order: Order, payment_id: str, confirmation_url: str) -> OrderResponseWithPayment:
    order_data = OrderResponse.model_validate(order).model_dump()
    order_data["payment_id"] = payment_id
    order_data["confirmation_url"] = confirmation_url
    return OrderResponseWithPayment.model_validate(order_data)
