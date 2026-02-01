from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    CartItemNotFoundError,
    CartNotFoundError,
    InsufficientPermissionError,
    ProductNotFoundError,
    UserCartMissingError,
)
from app.modules.discounts import service as discount_service
from app.modules.products import repository as product_repository
from app.modules.users.model import Role, User

from . import repository as cart_repository
from .schema import CartItemResponse, CartItemUpdate, CartResponse


async def get_current_user_cart(*, session: AsyncSession, user_id: int) -> CartResponse:
    """
    Возвращает корзину текущего пользователя.

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
    Удаляет корзину пользователя.

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
    *,
    session: AsyncSession,
    current_user: User,
    target_user_id: int | None = None,
    product_id: int,
    quantity: int,
) -> CartItemResponse:
    """
    Добавляет товар в корзину пользователя.

    Args:
        session: сессия базы данных
        current_user: активный пользователь
        target_user_id: пользователь, которому в корзину добавится товар
        product_id: идентификатор товара
        quantity: количество добавляемого товара

    Returns:
        CartItemResponse, данные об добавленном товаре

    Raises:
        ProductNotFoundError: не найден товар по ID
        InsufficientPermissionError: недостаточно прав для удаления корзины
    """
    if target_user_id and target_user_id != current_user.id:
        if current_user.role != Role.ADMIN:
            raise InsufficientPermissionError()
        user_id = target_user_id
    else:
        user_id = current_user.id

    product = await product_repository.get_product(session=session, product_id=product_id)
    if not product:
        raise ProductNotFoundError(product_id=product_id)

    discount_map = await discount_service.enrich_products(session=session, products=[product])
    discounted_price, _ = discount_map.get(product.id, (None, None))
    price = discounted_price if discounted_price is not None else product.price

    cart = await cart_repository.get_cart_by_user_id(session=session, user_id=user_id)
    if not cart:
        cart = await cart_repository.create_cart(session=session, user_id=user_id)

    cart_item_exists = await cart_repository.get_cart_item_for_update(
        session=session, cart_id=cart.id, product_id=product_id
    )
    if cart_item_exists:
        cart_item_exists.quantity += quantity
        await session.flush()
        return CartItemResponse.model_validate(cart_item_exists)

    try:
        cart_item = await cart_repository.create_cart_item(
            session=session,
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity,
            price=price,
        )
        return CartItemResponse.model_validate(cart_item)
    except IntegrityError:
        await session.rollback()
        cart_item_exists = await cart_repository.get_cart_item_for_update(
            session=session, cart_id=cart.id, product_id=product_id
        )
        if cart_item_exists:
            cart_item_exists.quantity += quantity
            await session.flush()
            return CartItemResponse.model_validate(cart_item_exists)
        raise


async def update_cart_item_quantity(
    *, session: AsyncSession, cart_item_id: int, quantity: int, current_user: User
) -> CartItemUpdate:
    """
    Изменяет количество конкретного товара в корзине пользователя.

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


async def delete_cart_item(*, session: AsyncSession, cart_item_id: int, current_user: User) -> None:
    """
    Удаляет товар из корзины.

    Args:
        session: сессия базы данных
        cart_item_id: идентификатор товара в корзине
        current_user: активный пользователь

    Returns:
        None

    Raises:
        CartItemNotFoundError: товар корзины по ID не найден
        InsufficientPermissionError: нет прав на удаление товара из чужой корзины
    """
    cart_item = await cart_repository.get_cart_item_by_id(session=session, cart_item_id=cart_item_id)
    if cart_item is None:
        raise CartItemNotFoundError(cart_item_id)

    if current_user.role != Role.ADMIN and cart_item.cart.user_id != current_user.id:
        raise InsufficientPermissionError()

    await cart_repository.delete_cart_item(session=session, cart_item_id=cart_item_id)
