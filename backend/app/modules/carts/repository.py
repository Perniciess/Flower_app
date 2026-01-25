from decimal import Decimal

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .model import Cart, CartItem


async def create_cart(*, session: AsyncSession, user_id: int) -> Cart:
    cart = Cart(user_id=user_id)
    session.add(cart)
    await session.flush()
    return cart


async def get_cart_by_user_id(*, session: AsyncSession, user_id: int) -> Cart | None:
    cart = select(Cart).options(selectinload(Cart.cart_item)).where(Cart.user_id == user_id)
    result = await session.execute(cart)
    return result.scalar_one_or_none()


async def get_cart_by_id(*, session: AsyncSession, cart_id: int) -> Cart | None:
    statement = select(Cart).options(selectinload(Cart.cart_item)).where(Cart.id == cart_id)
    cart = await session.execute(statement)
    return cart.scalar_one_or_none()


async def delete_cart(*, session: AsyncSession, cart_id: int) -> bool:
    statement = delete(Cart).where(Cart.id == cart_id).returning(Cart.id)
    result = await session.execute(statement)
    return result.scalar_one_or_none() is not None


async def create_cart_item(*, session: AsyncSession, cart_id: int, flower_id: int, quantity: int, price: Decimal) -> CartItem:
    cart_item = CartItem(cart_id=cart_id, flower_id=flower_id, quantity=quantity, price=price)
    session.add(cart_item)
    await session.flush()
    return cart_item


async def get_cart_item(*, session: AsyncSession, cart_id: int, flower_id: int) -> CartItem | None:
    statement = select(CartItem).where(CartItem.cart_id == cart_id, CartItem.flower_id == flower_id)
    cart_item = await session.execute(statement)
    return cart_item.scalar_one_or_none()


async def get_cart_item_by_id(*, session: AsyncSession, cart_item_id: int) -> CartItem | None:
    statement = select(CartItem).options(selectinload(CartItem.cart)).where(CartItem.id == cart_item_id)
    cart_item = await session.execute(statement)
    return cart_item.scalar_one_or_none()
