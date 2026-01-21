from sqlalchemy import delete, select
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


async def get_cart_by_id(session: AsyncSession, cart_id: int) -> Cart | None:
    statement = select(Cart).where(Cart.id == cart_id)
    cart = await session.execute(statement)
    return cart.scalar_one_or_none()


async def delete_cart(session: AsyncSession, cart_id: int) -> bool:
    statement = delete(Cart).where(Cart.id == cart_id).returning(Cart.id)
    result = await session.execute(statement)
    return result.scalar_one_or_none() is not None
