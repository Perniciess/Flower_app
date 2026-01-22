from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import CartAlreadyExistsException, CartNotFoundError
from app.modules.flowers import service as flower_service

from . import repository as cart_repository
from .schema import CartItemResponse, CartResponse


async def create_cart(*, session: AsyncSession, user_id: int) -> CartResponse:
    cart_exists = await cart_repository.get_cart_by_user_id(session=session, user_id=user_id)
    if cart_exists:
        raise CartAlreadyExistsException(cart_id=cart_exists.id)

    cart = await cart_repository.create_cart(session=session, user_id=user_id)
    return CartResponse.model_validate(cart)


async def delete_cart(*, session: AsyncSession, cart_id: int, user_id: int) -> bool:
    cart_exists = await cart_repository.get_cart_by_id(session=session, cart_id=cart_id)
    if not cart_exists:
        raise CartNotFoundError(cart_id=cart_id)
    deleted = await cart_repository.delete_cart(session=session, cart_id=cart_id)
    if not deleted:
        raise CartNotFoundError(cart_id=cart_id)
    return True


async def create_cart_item(*, session: AsyncSession, user_id: int, flower_id: int, quantity: int) -> CartItemResponse:
    cart = await cart_repository.get_cart_by_user_id(session=session, user_id=user_id)
    if not cart:
        cart = await cart_repository.create_cart(session=session, user_id=user_id)

    price = await flower_service.get_flower_price(session=session, flower_id=flower_id)

    cart_item_exists = await cart_repository.get_cart_item(session=session, cart_id=cart.id, flower_id=flower_id)
    if cart_item_exists:
        cart_item_exists.quantity += quantity
        await session.flush()
        return CartItemResponse.model_validate(cart_item_exists)

    cart_item = await cart_repository.create_cart_item(
        session=session, cart_id=cart.id, flower_id=flower_id, quantity=quantity, price=price
    )
    return CartItemResponse.model_validate(cart_item)
