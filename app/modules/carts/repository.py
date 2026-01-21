from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .model import Cart


async def create_cart(session: AsyncSession, user_id: int) -> Cart:
    cart = Cart(user_id=user_id)
    session.add(cart)
    await session.flush()
    return cart


async def get_cart_by_user_id(session: AsyncSession, user_id: int) -> Cart | None:
    cart = select(Cart).where(Cart.user_id == user_id)
    result = await session.execute(cart)
    return result.scalar_one_or_none()
