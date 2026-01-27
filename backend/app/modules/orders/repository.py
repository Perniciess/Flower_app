from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.carts.model import Cart, CartItem

from .model import Order, OrderItem, Status


async def create_order(*, session: AsyncSession, user_id: int, cart: Cart) -> Order:
    total_price = sum(item.quantity * item.price for item in cart.cart_item)

    order = Order(user_id=user_id, total_price=total_price, status=Status.PENDING)
    session.add(order)
    await session.flush()

    order_items = [
        OrderItem(
            order_id=order.id,
            flower_id=item.flower_id,
            quantity=item.quantity,
            price=item.price,
        )
        for item in cart.cart_item
    ]
    session.add_all(order_items)
    await session.flush()

    return order


async def clear_cart(*, session: AsyncSession, cart_id: int) -> None:
    await session.execute(delete(CartItem).where(CartItem.cart_id == cart_id))
