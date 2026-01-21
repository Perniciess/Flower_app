from sqlalchemy.ext.asyncio import AsyncSession

from . import repository as cart_repository


async def create_cart(session: AsyncSession, user_id: int):
    cart = await cart_repository.create_cart(session=session, user_id=user_id)
    return cart
