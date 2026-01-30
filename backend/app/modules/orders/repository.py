import uuid
from collections.abc import Sequence
from datetime import UTC, datetime

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.carts.model import Cart, CartItem

from .model import Order, OrderItem, Status


async def create_order(
    *,
    session: AsyncSession,
    user_id: int,
    cart: Cart,
    idempotency_key: uuid.UUID,
    expires_at: datetime,
) -> Order:
    total_price = sum(item.quantity * item.price for item in cart.cart_item)

    order = Order(
        user_id=user_id,
        total_price=total_price,
        idempotency_key=idempotency_key,
        expires_at=expires_at,
        status=Status.PENDING,
        order_item=[
            OrderItem(
                flower_id=item.flower_id,
                quantity=item.quantity,
                price=item.price,
            )
            for item in cart.cart_item
        ],
    )
    session.add(order)
    await session.flush()

    return order


async def clear_cart(*, session: AsyncSession, cart_id: int) -> None:
    await session.execute(delete(CartItem).where(CartItem.cart_id == cart_id))


async def get_pending_order_by_user_id(
    *, session: AsyncSession, user_id: int
) -> Order | None:
    statement = (
        select(Order)
        .options(selectinload(Order.order_item))
        .where(Order.user_id == user_id)
        .where(Order.status == Status.PENDING)
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def get_order_by_payment_id(
    *, session: AsyncSession, payment_id: str
) -> Order | None:
    statement = select(Order).where(Order.payment_id == payment_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def get_order_by_id(*, session: AsyncSession, order_id: int) -> Order | None:
    statement = (
        select(Order)
        .where(Order.id == order_id)
        .options(selectinload(Order.order_item))
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def get_orders(*, session: AsyncSession, user_id: int) -> Sequence[Order]:
    statement = select(Order).where(Order.user_id == user_id)
    result = await session.execute(statement)
    return result.scalars().all()


async def update_order_status(
    *, session: AsyncSession, order_id: int, status: Status
) -> Order | None:
    statement = (
        update(Order).where(Order.id == order_id).values(status=status).returning(Order)
    )
    result = await session.execute(statement)
    await session.flush()
    return result.scalar_one_or_none()


async def update_payment_id(
    *, session: AsyncSession, order_id: int, payment_id: str
) -> Order | None:
    statement = (
        update(Order)
        .where(Order.id == order_id)
        .values(payment_id=payment_id)
        .returning(Order)
    )
    result = await session.execute(statement)
    await session.flush()
    return result.scalar_one_or_none()


async def mark_order_paid(*, session: AsyncSession, order_id: int) -> Order | None:
    now = datetime.now(UTC)
    statement = (
        update(Order)
        .where(Order.id == order_id)
        .values(status=Status.PAID, paid_at=now)
        .returning(Order)
    )
    result = await session.execute(statement)
    await session.flush()
    return result.scalar_one_or_none()


async def get_expired_pending_orders(*, session: AsyncSession) -> Sequence[Order]:
    now = datetime.now(UTC)
    statement = (
        select(Order)
        .where(Order.status == Status.PENDING)
        .where(Order.expires_at < now)
    )
    result = await session.execute(statement)
    return result.scalars().all()
