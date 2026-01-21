from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import CartAlreadyExistsException, CartNotFoundError

from . import repository as cart_repository


async def create_cart(session: AsyncSession, user_id: int):
    cart_exists = await cart_repository.get_cart_by_user_id(session, user_id)
    if cart_exists:
        raise CartAlreadyExistsException(cart_id=cart_exists.id)
    return await cart_repository.create_cart(session=session, user_id=user_id)


async def delete_cart(*, session: AsyncSession, cart_id: int) -> bool:
    deleted = await cart_repository.delete_cart(session=session, cart_id=cart_id)
    if not deleted:
        raise CartNotFoundError(cart_id=cart_id)
    return True
