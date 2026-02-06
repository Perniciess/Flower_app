from collections.abc import Sequence

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_admin
from app.db.session import get_db
from app.models.users_model import User
from app.schemas.flowers_schema import FlowerCreate, FlowerResponse, FlowerUpdate
from app.service import flowers_service

flower_router = APIRouter(prefix="/flowers", tags=["flowers"])


@flower_router.post("", response_model=FlowerResponse, status_code=status.HTTP_201_CREATED)
async def create_flower(
    flower_data: FlowerCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> FlowerResponse:
    return await flowers_service.create_flower(session=session, flower_data=flower_data)


@flower_router.get("", response_model=Sequence[FlowerResponse], status_code=status.HTTP_200_OK)
async def get_flowers(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> Sequence[FlowerResponse]:
    return await flowers_service.get_flowers(session=session)


@flower_router.get("/{flower_id}", response_model=FlowerResponse, status_code=status.HTTP_200_OK)
async def get_flower(
    flower_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> FlowerResponse:
    return await flowers_service.get_flower(session=session, flower_id=flower_id)


@flower_router.patch("/{flower_id}", response_model=FlowerResponse, status_code=status.HTTP_200_OK)
async def update_flower(
    flower_id: int,
    flower_data: FlowerUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> FlowerResponse:
    return await flowers_service.update_flower(session=session, flower_id=flower_id, flower_data=flower_data)


@flower_router.delete("/{flower_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_flower(
    flower_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> None:
    await flowers_service.delete_flower(session=session, flower_id=flower_id)
