import uuid
from datetime import UTC, datetime
from decimal import Decimal

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    CartNotFoundError,
    EmptyCartError,
    InsufficientPermissionError,
    OrderNotFoundError,
    OrderNotUpdatedError,
)
from app.models.orders_model import Order, Status
from app.models.users_model import Role, User
from app.repository import carts_repository, orders_repository, products_repository
from app.schemas.orders_schema import (
    CreateOrderRequest,
    OrderResponse,
    OrderResponseWithPayment,
    WebhookPayload,
)
from app.service import discounts_service, payments_service, pickups_service


async def create_order(
    *,
    session: AsyncSession,
    data: CreateOrderRequest,
    user_id: int,
    idempotency_key: uuid.UUID,
    expires_at: datetime,
) -> OrderResponseWithPayment:
    """
    Создает заказ.

    Args:
        session: сессия базы данных
        data: данные для создания заказа
        user_id: идентификатор пользователя
        idempotency_key: уникальный ключ, чтобы не создавать дубликаты заказа и оплаты
        expires_at: время истечения оплаты заказа

    Returns:
        OrderResponseWithPayment с данными для оплаты заказа

    Raises:
        CartNotFoundError: если корзина пользователя не найдена
        EmptyCartError: если корзина пустая
    """
    cart = await carts_repository.get_cart_by_user_id(session=session, user_id=user_id)
    if cart is None:
        raise CartNotFoundError(user_id=user_id)

    if not cart.cart_item:
        raise EmptyCartError(cart_id=cart.id)

    if data.pickup_point_id is not None:
        await pickups_service.validate_pickup_point(session=session, pickup_point_id=data.pickup_point_id)

    product_ids = [item.product_id for item in cart.cart_item]
    products = await products_repository.get_products_by_ids(session=session, product_ids=product_ids)
    discount_map = await discounts_service.enrich_products(session=session, products=products)

    product_base_prices = {p.id: p.price for p in products}
    price_map: dict[int, Decimal] = {}
    for item in cart.cart_item:
        discounted_price, _ = discount_map.get(item.product_id, (None, None))
        price_map[item.product_id] = (
            discounted_price if discounted_price is not None else product_base_prices[item.product_id]
        )

    pending_order = await orders_repository.get_pending_order_by_user_id(session=session, user_id=user_id)
    if pending_order is not None:
        if pending_order.expires_at > datetime.now(UTC) and pending_order.payment_id is not None:
            payment_status, confirmation_url = payments_service.find_yookassa_payment(pending_order.payment_id)
            if payment_status == "pending" and confirmation_url is not None:
                return _build_response_with_payment(pending_order, pending_order.payment_id, confirmation_url)

        await orders_repository.update_order_status(session=session, order_id=pending_order.id, status=Status.CANCELLED)

    order = await orders_repository.create_order(
        session=session,
        user_id=user_id,
        data=data,
        cart=cart,
        price_map=price_map,
        idempotency_key=idempotency_key,
        expires_at=expires_at,
    )
    payment_id, confirmation_url = payments_service.create_yookassa_payment(
        amount=order.total_price, order_id=order.id, idempotency_key=idempotency_key
    )
    await orders_repository.update_payment_id(session=session, order_id=order.id, payment_id=payment_id)

    return _build_response_with_payment(order, payment_id, confirmation_url)


async def process_webhook(*, session: AsyncSession, payload: WebhookPayload) -> None:
    """
    Если оплата прошла, то помечает заказ как оплаченный и очищает корзину пользователя.
    Если оплату отменили, то обновляет статус заказа как отмененный.

    Args:
        session: сессия базы данных
        payload: данные об уведомлении от юkassa
    Returns:
        None
    """
    order = await orders_repository.get_order_by_payment_id(session=session, payment_id=payload.object.id)
    if order is None:
        return

    if order.status != Status.PENDING:
        return  # Already processed — idempotent

    if payload.event == "payment.succeeded":
        await orders_repository.mark_order_paid(session=session, order_id=order.id)
        cart = await carts_repository.get_cart_by_user_id(session=session, user_id=order.user_id)
        if cart is not None:
            await carts_repository.clear_cart(session=session, cart_id=cart.id)
    elif payload.event == "payment.canceled":
        await orders_repository.update_order_status(session=session, order_id=order.id, status=Status.CANCELLED)


async def get_orders(session: AsyncSession, user_id: int) -> Page[OrderResponse]:
    """
    Возвращает пагинированный список заказов.

    Args:
        session: сессия базы данных
        user_id: идентификатор пользователя
    Returns:
        Page[OrderResponse] список заказов пользователя
    """
    query = orders_repository.get_orders_query(user_id=user_id)
    return await paginate(session, query)


async def get_order_by_id(session: AsyncSession, order_id: int, current_user: User) -> OrderResponse:
    """
    Возвращает заказ.

    Args:
        session: сессия базы данных
        order_id: идентификатор заказа
    Returns:
        OrderResponse информация о заказе
    """
    order = await orders_repository.get_order_by_id(session=session, order_id=order_id)
    if order is None:
        raise OrderNotFoundError(order_id=order_id)
    if order.user_id != current_user.id and current_user.role != Role.ADMIN:
        raise InsufficientPermissionError()
    return OrderResponse.model_validate(order)


async def update_order_status(session: AsyncSession, order_id: int, status: Status) -> OrderResponse:
    """
    Изменяет статус заказа.

    Args:
        session: сессия базы данных
        order_id: идентификатор заказа
        status: новый статус заказа
    Returns:
        OrderResponse информация о заказе

    Raises:
        OrderNotFoundError: если заказ не найден
        OrderNotUpdatedError: если не удалось обновить статус
    """
    order = await orders_repository.get_order_by_id(session=session, order_id=order_id)
    if order is None:
        raise OrderNotFoundError(order_id=order_id)
    updated = await orders_repository.update_order_status(session=session, order_id=order_id, status=status)
    if updated is None:
        raise OrderNotUpdatedError(order_id=order_id)

    return OrderResponse.model_validate(updated)


async def cancel_order(session: AsyncSession, order_id: int, user_id: int) -> OrderResponse:
    order = await orders_repository.get_order_by_id(session=session, order_id=order_id)
    if order is None:
        raise OrderNotFoundError(order_id=order_id)
    if order.user_id != user_id:
        raise InsufficientPermissionError()
    if order.status not in (Status.PENDING, Status.PAID):
        raise OrderNotUpdatedError(order_id=order_id)

    updated = await orders_repository.update_order_status(session=session, order_id=order_id, status=Status.CANCELLED)
    if updated is None:
        raise OrderNotUpdatedError(order_id=order_id)
    return OrderResponse.model_validate(updated)


async def get_all_orders(session: AsyncSession) -> Page[OrderResponse]:
    """
    Возвращает пагинированный список заказов.

    Args:
        session: сессия базы данных
    Returns:
        Page[OrderResponse] список заказов
    """
    query = orders_repository.get_all_orders_query()
    return await paginate(session, query)


async def get_all_paid_orders(session: AsyncSession) -> Page[OrderResponse]:
    """
    Возвращает пагинированный список оплаченных заказов.

    Args:
        session: сессия базы данных
    Returns:
        Page[OrderResponse]
    """
    query = orders_repository.get_all_paid_query()
    return await paginate(session, query)


def _build_response_with_payment(order: Order, payment_id: str, confirmation_url: str) -> OrderResponseWithPayment:
    """
    Собирает ответ заказа с данными оплаты.

    Args:
        order: заказ пользователя
        payment_id: идентификатор оплаты
        confirmation_url: ссылка на оплату юkassa
    Returns:
        OrderResponseWithPayment: информация для оплаты
    """
    order_data = OrderResponse.model_validate(order).model_dump()
    order_data["payment_id"] = payment_id
    order_data["confirmation_url"] = confirmation_url
    return OrderResponseWithPayment.model_validate(order_data)
