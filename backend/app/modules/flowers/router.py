from collections.abc import Sequence

from fastapi import APIRouter, Depends, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_admin
from app.database.session import get_db
from app.modules.users.model import User

from . import service as flower_service
from .schema import FlowerCreate, FlowerImageResponse, FlowerResponse, FlowerUpdate

flower_router = APIRouter(prefix="/flowers", tags=["flowers"])


@flower_router.post("/create", response_model=FlowerResponse, summary="Создать цветок")
async def create_flower(
    flower_data: FlowerCreate, session: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)
) -> FlowerResponse:
    """
    Создание цветка

    Требует прав администратора
    """
    flower = await flower_service.create_flower(session=session, flower_data=flower_data)
    return flower


@flower_router.get("/", response_model=Sequence[FlowerResponse], summary="Получить список цветов")
async def get_flowers(session: AsyncSession = Depends(get_db)) -> Sequence[FlowerResponse]:
    """Получение списка цветов"""
    flowers = await flower_service.get_flowers(session=session)
    return flowers


@flower_router.patch("/{flower_id}", response_model=FlowerResponse, summary="Получить цветок по ID")
async def update_flower(
    flower_id: int, flower_data: FlowerUpdate, session: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)
) -> FlowerResponse:
    """
    Изменение информации о цветке.

    Требует прав администратора.
    """
    flower = await flower_service.update_flower(session=session, flower_id=flower_id, flower_data=flower_data)
    return flower


@flower_router.delete("/{flower_id}", status_code=204, summary="Удалить цветок")
async def delete_flower(flower_id: int, session: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)):
    """
    Удаление цветка.

    Требует прав администратора.
    """
    await flower_service.delete_flower(session=session, flower_id=flower_id)


@flower_router.post("/images/{flower_id}", response_model=FlowerImageResponse, summary="Загрузить изображение цветка")
async def upload_image(
    flower_id: int,
    image: UploadFile,
    sort_order: int = Form(default=0),
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> FlowerImageResponse:
    """
    Добавление изображения цветка.

    Требует прав администратора.
    """
    flower_image = await flower_service.upload_image(session=session, flower_id=flower_id, image=image, sort_order=sort_order)
    return flower_image


@flower_router.get("/images", response_model=Sequence[FlowerImageResponse], summary="Получить изображения цветка")
async def get_flowers_images(session: AsyncSession = Depends(get_db)) -> Sequence[FlowerImageResponse]:
    """Получение изображений цветка."""
    images = await flower_service.get_flowers_images(session=session)
    return images


@flower_router.delete("/images/{image_id}", status_code=204, summary="Удалить изображение цветка")
async def delete_flower_image(image_id: int, session: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)):
    """
    Удаление изображения цветка.

    Требует прав администратора.
    """
    await flower_service.delete_flower_image(session=session, image_id=image_id)
