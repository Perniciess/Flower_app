from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import CartNotFoundError
from app.modules.carts.service import cart_repository

from . import repository as order_repository
from .schema import OrderResponse


async def create_order(*, session: AsyncSession, user_id: int) -> OrderResponse:
    cart = await cart_repository.get_cart_by_user_id(session=session, user_id=user_id)
    if cart is None:
        raise CartNotFoundError(user_id=user_id)
    order = await order_repository.create_order(session=session, user_id=user_id, cart=cart)
    return OrderResponse.model_validate(order)
