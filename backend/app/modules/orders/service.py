import uuid
from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import CartNotFoundError, EmptyCartError
from app.modules.carts import repository as cart_repository
from app.modules.payments import service as payment_service

from . import repository as order_repository
from .model import Status
from .schema import OrderResponse


async def create_order(*, session: AsyncSession, user_id: int, idempotency_key: uuid.UUID, expires_at: datetime) -> OrderResponse:
    cart = await cart_repository.get_cart_by_user_id(session=session, user_id=user_id)
    if cart is None:
        raise CartNotFoundError(user_id=user_id)

    if not cart.cart_item:
        raise EmptyCartError(cart_id=cart.id)

    pending_order = await order_repository.get_pending_order_by_user_id(session=session, user_id=user_id)
    if pending_order is not None:
        if pending_order.expires_at > datetime.now(UTC):
            return ...
        else:
            await order_repository.update_order_status(session=session, order_id=pending_order.id, status=Status.CANCELLED)

    order = await order_repository.create_order(
        session=session, user_id=user_id, cart=cart, idempotency_key=idempotency_key, expires_at=expires_at
    )
    payment_id, confirmation_url = await payment_service.create_yookassa_payment(
        amount=order.total_price, order_id=order.id, idempotency_key=idempotency_key
    )
    await order_repository.update_payment_id(session=session, order_id=order.id, payment_id=payment_id)

    return OrderResponse.model_validate(order)
