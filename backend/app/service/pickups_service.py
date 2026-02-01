"""Сервис для работы с точками самовывоза."""

from collections.abc import Sequence

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import PickupPointNotActiveError, PickupPointNotFoundError
from app.models.pickups_model import PickupPoint
from app.repository import pickups_repository
from app.schemas.pickups_schema import PickupPointCreate, PickupPointResponse, PickupPointUpdate


async def create_pickup_point(session: AsyncSession, data: PickupPointCreate) -> PickupPointResponse:
    """Создать точку самовывоза.

    Args:
        session: Сессия базы данных.
        data: Данные для создания точки самовывоза.

    Returns:
        Созданная точка самовывоза.
    """
    pickup_point = await pickups_repository.create_pickup_point(session, data)
    return PickupPointResponse.model_validate(pickup_point)


async def get_pickup_point_by_id(session: AsyncSession, pickup_point_id: int) -> PickupPointResponse:
    """Получить точку самовывоза по ID.

    Args:
        session: Сессия базы данных.
        pickup_point_id: ID точки самовывоза.

    Returns:
        Точка самовывоза.

    Raises:
        PickupPointNotFoundError: Если точка самовывоза не найдена.
    """
    pickup_point = await pickups_repository.get_pickup_point_by_id(session, pickup_point_id)
    if not pickup_point:
        raise PickupPointNotFoundError(pickup_point_id)

    return PickupPointResponse.model_validate(pickup_point)


async def get_all_active_pickup_points(session: AsyncSession) -> Sequence[PickupPointResponse]:
    """Получить все активные точки самовывоза.

    Args:
        session: Сессия базы данных.

    Returns:
        Список активных точек самовывоза.
    """
    pickup_points = await pickups_repository.get_all_active_pickup_points(session)
    return [PickupPointResponse.model_validate(pp) for pp in pickup_points]


async def get_all_pickup_points(session: AsyncSession) -> Page[PickupPointResponse]:
    """Получить все точки самовывоза с пагинацией.

    Args:
        session: Сессия базы данных.

    Returns:
        Пагинированный список всех точек самовывоза.
    """
    query = pickups_repository.get_all_pickup_points_query()
    return await paginate(session, query)


async def update_pickup_point(
    session: AsyncSession, pickup_point_id: int, data: PickupPointUpdate
) -> PickupPointResponse:
    """Обновить точку самовывоза.

    Args:
        session: Сессия базы данных.
        pickup_point_id: ID точки самовывоза.
        data: Новые данные.

    Returns:
        Обновленная точка самовывоза.

    Raises:
        PickupPointNotFoundError: Если точка самовывоза не найдена.
    """
    pickup_point = await pickups_repository.get_pickup_point_by_id(session, pickup_point_id)
    if not pickup_point:
        raise PickupPointNotFoundError(pickup_point_id)

    updated_pickup_point = await pickups_repository.update_pickup_point(session, pickup_point, data)
    return PickupPointResponse.model_validate(updated_pickup_point)


async def delete_pickup_point(session: AsyncSession, pickup_point_id: int) -> None:
    """Удалить точку самовывоза.

    Args:
        session: Сессия базы данных.
        pickup_point_id: ID точки самовывоза.

    Raises:
        PickupPointNotFoundError: Если точка самовывоза не найдена.
    """
    pickup_point = await pickups_repository.get_pickup_point_by_id(session, pickup_point_id)
    if not pickup_point:
        raise PickupPointNotFoundError(pickup_point_id)

    await pickups_repository.delete_pickup_point(session, pickup_point_id)


async def validate_pickup_point(session: AsyncSession, pickup_point_id: int) -> PickupPoint:
    """Валидировать точку самовывоза для создания заказа.

    Args:
        session: Сессия базы данных.
        pickup_point_id: ID точки самовывоза.

    Returns:
        Точка самовывоза.

    Raises:
        PickupPointNotFoundError: Если точка самовывоза не найдена.
        PickupPointNotActiveError: Если точка самовывоза неактивна.
    """
    pickup_point = await pickups_repository.get_pickup_point_by_id(session, pickup_point_id)
    if not pickup_point:
        raise PickupPointNotFoundError(pickup_point_id)

    if not pickup_point.is_active:
        raise PickupPointNotActiveError(pickup_point_id)

    return pickup_point
