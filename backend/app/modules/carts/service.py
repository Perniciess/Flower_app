from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    CartItemNotFoundError,
    CartNotFoundError,
    InsufficientPermissionError,
    UserCartMissingError,
)
from app.modules.flowers import service as flower_service
from app.modules.users.model import Role, User

from . import repository as cart_repository
from .schema import CartItemResponse, CartItemUpdate, CartResponse


async def get_current_user_cart(*, session: AsyncSession, user_id: int) -> CartResponse:
    """
    Получение корзины текущего пользователя.

    Args:
        session: сессия базы данных
        user_id: идентификатор пользователя

    Returns:
        CartResponse о корзине пользователя

    Raises:
        UserCartMissingError: у пользователя нет корзины
    """
    cart = await cart_repository.get_cart_by_user_id(session=session, user_id=user_id)
    if cart is None:
        raise UserCartMissingError(user_id=user_id)
    return CartResponse.model_validate(cart)


async def delete_cart(*, session: AsyncSession, cart_id: int) -> None:
    """
    Удаление корзины пользователя.

    Args:
        session: сессия базы данных
        cart_id: идентификатор корзины

    Returns:
        None

    Raises:
        CartNotFoundError: корзина по ID не найдена
    """
    cart_exists = await cart_repository.get_cart_by_id(session=session, cart_id=cart_id)
    if not cart_exists:
        raise CartNotFoundError(cart_id=cart_id)
    deleted = await cart_repository.delete_cart(session=session, cart_id=cart_id)
    if not deleted:
        raise CartNotFoundError(cart_id=cart_id)


async def create_cart_item(
    *, session: AsyncSession, current_user: User, target_user_id: int | None = None, flower_id: int, quantity: int
) -> CartItemResponse:
    """
    Добавление товара в корзину пользователя.

    Args:
        session: сессия базы данных
        current_user: активный пользователь
        target_user_id: пользователь, которому в корзину добавится товар

    Returns:
        CartItemResponse, данные об добавленном товаре

    Raises:
        CartNotFoundError: корзина по ID не найдена
    """
    if target_user_id and target_user_id != current_user.id:
        if current_user.role != Role.ADMIN:
            raise InsufficientPermissionError()
        user_id = target_user_id
    else:
        user_id = current_user.id

    price = await flower_service.get_flower_price(session=session, flower_id=flower_id)

    cart = await cart_repository.get_cart_by_user_id(session=session, user_id=user_id)
    if not cart:
        cart = await cart_repository.create_cart(session=session, user_id=user_id)

    cart_item_exists = await cart_repository.get_cart_item(session=session, cart_id=cart.id, flower_id=flower_id)
    if cart_item_exists:
        cart_item_exists.quantity += quantity
        await session.flush()
        return CartItemResponse.model_validate(cart_item_exists)

    cart_item = await cart_repository.create_cart_item(
        session=session, cart_id=cart.id, flower_id=flower_id, quantity=quantity, price=price
    )
    return CartItemResponse.model_validate(cart_item)


async def update_cart_item_quantity(*, session: AsyncSession, cart_item_id: int, quantity: int, current_user: User) -> CartItemUpdate:
    """
    Увеличение количества конкретного товара в корзине пользователя.

    Args:
        session: сессия базы данных
        current_user: активный пользователь
        cart_item_id: идентификтаор товара в корзине
        quantity: на сколько нужно увеличить

    Returns:
        CartItemResponse, данные об добавленном товаре

    Raises:
        CartNotFoundError: корзина по ID не найдена
        InsufficientPermissionError: нет прав на изменение корзины
    """
    cart_item = await cart_repository.get_cart_item_by_id(session=session, cart_item_id=cart_item_id)
    if cart_item is None:
        raise CartItemNotFoundError(cart_item_id)

    if current_user.role != Role.ADMIN and cart_item.cart.user_id != current_user.id:
        raise InsufficientPermissionError()

    cart_item.quantity = quantity
    await session.flush()
    return CartItemUpdate.model_validate(cart_item)
