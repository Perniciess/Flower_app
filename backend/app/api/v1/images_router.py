from collections.abc import Sequence

from fastapi import APIRouter, Body, Depends, UploadFile, status
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_admin
from app.db.session import get_db
from app.models.users_model import User
from app.schemas.image_schema import ImageResponse, ImageUpdate
from app.service import images_service

image_router = APIRouter(prefix="/images", tags=["images"])


@image_router.post(
    "/upload",
    response_model=ImageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Загрузить изображение",
)
async def create_image(
    img: UploadFile,
    type: str = Body(),
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> ImageResponse:
    """
    Загрузить изображение.

    Требует прав администратора.
    """
    image = await images_service.create_image(session=session, type=type, image=img)

    return image


@image_router.get(
    "/all",
    response_model=Sequence[ImageResponse],
    status_code=status.HTTP_200_OK,
    summary="Получить все изображения",
)
async def get_images(
    session: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)
) -> Sequence[ImageResponse]:
    images = await images_service.get_images(session=session)
    return images


@image_router.get(
    "",
    response_model=Page[ImageResponse],
    status_code=status.HTTP_200_OK,
    summary="Получить пагинированный список изображений",
)
async def get_images_query(
    session: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)
) -> Page[ImageResponse]:
    images = await images_service.get_images_query(session=session)
    return images


@image_router.patch(
    "/{image_id}",
    response_model=ImageResponse,
    status_code=status.HTTP_200_OK,
    summary="Обновить изображение",
)
async def update_image(
    image_id: int,
    image_data: ImageUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> ImageResponse:
    """
    Обновить информации об изображение.

    Требует прав администратора.
    """
    return await images_service.update_image(
        session=session, image_id=image_id, image_data=image_data
    )


@image_router.delete(
    "/{image_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить изображение"
)
async def delete_image(
    image_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> None:
    """
    Удалить изображение.

    Требует прав администратора.
    """
    await images_service.delete_image(session=session, image_id=image_id)
