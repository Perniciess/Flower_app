from sqlalchemy.ext.asyncio import AsyncSession

from .model import Cart


async def create_cart(session: AsyncSession, user_id: int) -> Cart:
    cart = Cart(user_id=user_id)
    session.add(cart)
    await session.flush()
    return cart
