from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_admin
from app.database.session import get_db
from app.modules.users.model import User

from . import service as discount_service
from .schema import DiscountCreate, DiscountResponse, DiscountUpdate

discount_router = APIRouter(prefix="/discounts", tags=["discounts"])


@discount_router.post("", response_model=DiscountResponse, status_code=status.HTTP_201_CREATED, summary="Создать акцию")
async def create_discount(
    discount_data: DiscountCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> DiscountResponse:
    """
    Создать акцию.

    Требует прав администратора.
    """
    return await discount_service.create_discount(session=session, discount_data=discount_data)


@discount_router.get("", response_model=Page[DiscountResponse], status_code=status.HTTP_200_OK, summary="Список всех акций")
async def get_discounts(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> Page[DiscountResponse]:
    """
    Получить список всех акций.

    Требует прав администратора.
    """
    return await discount_service.get_discounts(session=session)


@discount_router.get("/{discount_id}", response_model=DiscountResponse, status_code=status.HTTP_200_OK, summary="Получить акцию по ID")
async def get_discount(
    discount_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> DiscountResponse:
    """
    Получить акцию по ID.

    Требует прав администратора.
    """
    return await discount_service.get_discount(session=session, discount_id=discount_id)


@discount_router.patch("/{discount_id}", response_model=DiscountResponse, status_code=status.HTTP_200_OK, summary="Обновить акцию")
async def update_discount(
    discount_id: int,
    discount_data: DiscountUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> DiscountResponse:
    """
    Обновить информации об акции.

    Требует прав администратора.
    """
    return await discount_service.update_discount(session=session, discount_id=discount_id, discount_data=discount_data)


@discount_router.delete("/{discount_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить акцию")
async def delete_discount(
    discount_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> None:
    """
    Удалить акцию.

    Требует прав администратора.
    """
    await discount_service.delete_discount(session=session, discount_id=discount_id)
