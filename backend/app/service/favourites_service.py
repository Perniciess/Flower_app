from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import FavouriteItemAlreadyExistsError, FavouriteItemNotFoundError, ProductNotFoundError
from app.repository import favourites_repository, products_repository
from app.schemas.favourites_schema import FavouriteResponse


async def add_to_favourite(*, session: AsyncSession, product_id: int, user_id: int) -> FavouriteResponse:
    """
    Добавляет товар в избранный список товаров пользователя.

    Args:
        session: сессия базы данных
        product_id: идентификатор товара
        user_id: идентификатор пользователя

    Returns:
        FavouriteResponse данные о добавленном товаре

    Raises:
        ProductNotFoundError: если товар не найден
        FavouriteItemAlreadyExistsError: если товар уже находится в списке избранных
    """
    product_exist = await products_repository.get_product(session=session, product_id=product_id)
    if product_exist is None:
        raise ProductNotFoundError(product_id=product_id)

    favourite_exist = await favourites_repository.get_favourite_by_product(
        session=session, user_id=user_id, product_id=product_id
    )
    if favourite_exist is not None:
        raise FavouriteItemAlreadyExistsError(product_id=product_id)

    favourite = await favourites_repository.add_to_favourite(session=session, product_id=product_id, user_id=user_id)
    return FavouriteResponse.model_validate(favourite)


async def get_favourite_list(*, session: AsyncSession, user_id: int) -> Sequence[FavouriteResponse]:
    """
    Возвращает список избранных товаров пользователя.

    Args:
        session: сессия базы данных
        user_id: идентификатор пользователя

    Returns:
        Sequence[FavouriteResponse] список избранных товаров пользователя
    """
    favourites = await favourites_repository.get_favourite_list(session=session, user_id=user_id)
    return [FavouriteResponse.model_validate(favourite) for favourite in favourites]


async def delete_from_favourites(*, session: AsyncSession, user_id: int, product_id: int) -> bool:
    """
    Удаляет товар из избранных.

    Args:
        session: сессия базы данных
        product_id: идентификатор товара
        user_id: идентификатор пользователя

    Returns:
        bool: удален товар или нет
    Raises:
        FavouriteItemNotFoundError: если товар в списке избранных не найден
    """
    deleted = await favourites_repository.delete_from_favourite(session=session, user_id=user_id, product_id=product_id)
    if not deleted:
        raise FavouriteItemNotFoundError(product_id=product_id)
    return True
