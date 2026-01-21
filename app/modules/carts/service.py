from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import CartAlreadyExistsException

from . import repository as cart_repository


async def create_cart(session: AsyncSession, user_id: int):
    cart_exist = await cart_repository.get_cart_by_user_id(session, user_id)
    if cart_exist:
        raise CartAlreadyExistsException(cart_id=cart_exist.id)
    return await cart_repository.create_cart(session=session, user_id=user_id)
