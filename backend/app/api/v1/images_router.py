from fastapi import APIRouter, Body, Depends, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_admin
from app.db.session import get_db
from app.models.users_model import User
from app.schemas.image_schema import ImageResponse
from app.service import images_service

image_router = APIRouter(prefix="/images", tags=["images"])


@image_router.post(
    "/upload",
    response_model=ImageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Загрузить изображение",
)
async def create_product(
    image: UploadFile,
    type: str = Body(),
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> ImageResponse:
    """
    Загрузить изображение.

    Требует прав администратора.
    """
    product = await images_service.create_image(session=session, type=type, image=image)

    return product
