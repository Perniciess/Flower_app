from collections.abc import Sequence

from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_admin
from app.db.session import get_db
from app.models.users_model import User
from app.schemas.pickups_schema import PickupPointCreate, PickupPointResponse, PickupPointUpdate
from app.service import pickups_service

pickup_point_router = APIRouter(prefix="/pickup-points", tags=["pickup_points"])


@pickup_point_router.post(
    "/create",
    response_model=PickupPointResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать точку самовывоза",
)
async def create_pickup_point(
    data: PickupPointCreate,
    session: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
) -> PickupPointResponse:
    """
    Создать точку самовывоза.

    Требует прав администратора.
    """
    return await pickups_service.create_pickup_point(session, data)


@pickup_point_router.get(
    "/active",
    response_model=list[PickupPointResponse],
    status_code=status.HTTP_200_OK,
)
async def get_active_pickup_points(
    session: AsyncSession = Depends(get_db),
) -> Sequence[PickupPointResponse]:
    """
    Получить все активные точки самовывоза.
    """
    return await pickups_service.get_all_active_pickup_points(session)


@pickup_point_router.get(
    "/all",
    response_model=Page[PickupPointResponse],
    status_code=status.HTTP_200_OK,
    summary="Получить все точки самовывоза",
)
async def get_all_pickup_points(
    session: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
) -> Page[PickupPointResponse]:
    """
    Получить все точки самовывоза.
    """
    return await pickups_service.get_all_pickup_points(session)


@pickup_point_router.get(
    "/{pickup_point_id}",
    response_model=PickupPointResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить точку самовывоза по ID",
)
async def get_pickup_point(
    pickup_point_id: int,
    session: AsyncSession = Depends(get_db),
) -> PickupPointResponse:
    """
    Получить точку самовывоза по ID.
    """
    return await pickups_service.get_pickup_point_by_id(session, pickup_point_id)


@pickup_point_router.patch(
    "/{pickup_point_id}",
    response_model=PickupPointResponse,
    status_code=status.HTTP_200_OK,
    summary="Обновить точку самовывоза",
)
async def update_pickup_point(
    pickup_point_id: int,
    data: PickupPointUpdate,
    session: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
) -> PickupPointResponse:
    """
    Обновить точку самовывоза.

    Требует права администратора.
    """
    return await pickups_service.update_pickup_point(session, pickup_point_id, data)


@pickup_point_router.delete(
    "/{pickup_point_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить точку самовывоза",
)
async def delete_pickup_point(
    pickup_point_id: int,
    session: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
) -> None:
    """
    Удалить точку самовывоза.

    Требует права администратора.
    """
    await pickups_service.delete_pickup_point(session, pickup_point_id)
