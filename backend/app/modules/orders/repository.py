import uuid
from collections.abc import Sequence
from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy import Select, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.carts.model import Cart

from .model import Delivery, Order, OrderItem, Status
from .schema import CreateOrderRequest


async def create_order(
    *,
    session: AsyncSession,
    data: CreateOrderRequest,
    user_id: int,
    cart: Cart,
    price_map: dict[int, Decimal],
    idempotency_key: uuid.UUID,
    expires_at: datetime,
) -> Order:
    total_price = sum(item.quantity * price_map[item.product_id] for item in cart.cart_item)

    delivery = None
    if data.delivery is not None:
        delivery = Delivery(
            address=data.delivery.address,
            recipient_name=data.delivery.recipient_name,
            recipient_phone=data.delivery.recipient_phone,
            comment=data.delivery.comment,
        )

    order = Order(
        user_id=user_id,
        total_price=total_price,
        method_of_receipt=data.method_of_receipt,
        idempotency_key=idempotency_key,
        expires_at=expires_at,
        status=Status.PENDING,
        order_item=[
            OrderItem(
                product_id=item.product_id,
                quantity=item.quantity,
                price=price_map[item.product_id],
            )
            for item in cart.cart_item
        ],
        delivery=delivery,
    )
    session.add(order)
    await session.flush()

    return order


async def get_pending_order_by_user_id(*, session: AsyncSession, user_id: int) -> Order | None:
    statement = (
        select(Order)
        .options(selectinload(Order.order_item))
        .where(Order.user_id == user_id)
        .where(Order.status == Status.PENDING)
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def get_order_by_payment_id(*, session: AsyncSession, payment_id: str) -> Order | None:
    statement = select(Order).where(Order.payment_id == payment_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def get_order_by_id(*, session: AsyncSession, order_id: int) -> Order | None:
    statement = (
        select(Order).where(Order.id == order_id).options(selectinload(Order.order_item), selectinload(Order.delivery))
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none()


def get_orders_query(user_id: int) -> Select[tuple[Order]]:
    return (
        select(Order)
        .options(selectinload(Order.order_item), selectinload(Order.delivery))
        .where(Order.user_id == user_id)
        .order_by(Order.id)
    )


def get_all_orders_query() -> Select[tuple[Order]]:
    return select(Order).options(selectinload(Order.order_item), selectinload(Order.delivery)).order_by(Order.id)


def get_all_paid_query() -> Select[tuple[Order]]:
    return (
        select(Order)
        .options(selectinload(Order.order_item), selectinload(Order.delivery))
        .where(Order.status == Status.PAID)
        .order_by(Order.id)
    )


async def update_order_status(*, session: AsyncSession, order_id: int, status: Status) -> Order | None:
    statement = update(Order).where(Order.id == order_id).values(status=status).returning(Order)
    result = await session.execute(statement)
    await session.flush()
    return result.scalar_one_or_none()


async def update_payment_id(*, session: AsyncSession, order_id: int, payment_id: str) -> Order | None:
    statement = update(Order).where(Order.id == order_id).values(payment_id=payment_id).returning(Order)
    result = await session.execute(statement)
    await session.flush()
    return result.scalar_one_or_none()


async def mark_order_paid(*, session: AsyncSession, order_id: int) -> Order | None:
    now = datetime.now(UTC)
    statement = update(Order).where(Order.id == order_id).values(status=Status.PAID, paid_at=now).returning(Order)
    result = await session.execute(statement)
    await session.flush()
    return result.scalar_one_or_none()


async def get_expired_pending_orders(*, session: AsyncSession) -> Sequence[Order]:
    now = datetime.now(UTC)
    statement = select(Order).where(Order.status == Status.PENDING).where(Order.expires_at < now)
    result = await session.execute(statement)
    return result.scalars().all()
