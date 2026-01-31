from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, require_admin
from app.modules.users.model import User

from . import service as discount_service
from .schema import DiscountCreate, DiscountResponse, DiscountUpdate

discount_router = APIRouter(prefix="/discounts", tags=["discounts"])


@discount_router.post("", response_model=DiscountResponse, summary="Создать скидку")
async def create_discount(
    discount_data: DiscountCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> DiscountResponse:
    return await discount_service.create_discount(session=session, discount_data=discount_data)


@discount_router.get("", response_model=Page[DiscountResponse], summary="Список всех скидок")
async def get_discounts(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> Page[DiscountResponse]:
    return await discount_service.get_discounts(session=session)


@discount_router.get("/{discount_id:int}", response_model=DiscountResponse, summary="Получить скидку по ID")
async def get_discount(
    discount_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> DiscountResponse:
    return await discount_service.get_discount(session=session, discount_id=discount_id)


@discount_router.patch("/{discount_id:int}", response_model=DiscountResponse, summary="Обновить скидку")
async def update_discount(
    discount_id: int,
    discount_data: DiscountUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> DiscountResponse:
    return await discount_service.update_discount(session=session, discount_id=discount_id, discount_data=discount_data)


@discount_router.delete("/{discount_id:int}", status_code=204, summary="Удалить скидку")
async def delete_discount(
    discount_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> None:
    await discount_service.delete_discount(session=session, discount_id=discount_id)
