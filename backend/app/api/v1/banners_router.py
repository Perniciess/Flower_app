from collections.abc import Sequence

from fastapi import APIRouter, Depends, Form, Request, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_admin
from app.core.limiter import limiter
from app.db.session import get_db
from app.models.users_model import User
from app.schemas.banners_schema import BannerCreate, BannerResponse, BannerUpdate
from app.service import banners_service

banner_router = APIRouter(prefix="/banners", tags=["banners"])


@banner_router.post(
    "",
    response_model=BannerResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать баннер",
)
async def create_banner(
    title: str = Form(...),
    description: str = Form(...),
    link: str = Form(default=None),
    sort_order: int = Form(default=0),
    is_active: bool = Form(default=False),
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
    image: UploadFile | None = None,
) -> BannerResponse:
    """
    Создать баннер

    Требует прав администратора
    """
    banner_data = BannerCreate(
        title=title,
        description=description,
        link=link,
        sort_order=sort_order,
        is_active=is_active,
    )
    return await banners_service.create_banner(
        session=session, banner_data=banner_data, image=image
    )


@banner_router.get(
    "",
    response_model=Sequence[BannerResponse],
    status_code=status.HTTP_200_OK,
    summary="Получить список активных баннеров",
)
@limiter.limit("60/minute")
async def get_banners(
    request: Request,
    only_active: bool = True,
    session: AsyncSession = Depends(get_db),
) -> Sequence[BannerResponse]:
    """
    Получить список активных баннеров.
    """
    return await banners_service.get_banners(session=session, only_active=only_active)


@banner_router.get(
    "/all",
    response_model=Sequence[BannerResponse],
    status_code=status.HTTP_200_OK,
    summary="Получить список всех баннеров",
)
async def get_all_banners(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> Sequence[BannerResponse]:
    """
    Получить список всех баннеров.

    Требует прав администратора.
    """
    return await banners_service.get_banners(session=session, only_active=False)


@banner_router.get(
    "/{banner_id}",
    response_model=BannerResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить баннер",
)
async def get_banner(
    banner_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> BannerResponse:
    """
    Получить баннер.

    Требует прав администратора.
    """
    return await banners_service.get_banner(session=session, banner_id=banner_id)


@banner_router.patch(
    "/{banner_id}",
    response_model=BannerResponse,
    status_code=status.HTTP_200_OK,
    summary="Обновить баннер",
)
async def update_banner(
    banner_id: int,
    banner_data: BannerUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> BannerResponse:
    """
    Изменить данные баннера.

    Требует прав администратора.
    """
    return await banners_service.update_banner(
        session=session, banner_id=banner_id, banner_data=banner_data
    )


@banner_router.post(
    "/{banner_id}/image",
    response_model=BannerResponse,
    status_code=status.HTTP_200_OK,
    summary="Загрузить изображение баннера",
)
async def upload_banner_image(
    banner_id: int,
    image: UploadFile,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> BannerResponse:
    """
    Загрузить изображение баннера.

    Требует прав администратора.
    """
    return await banners_service.upload_image(
        session=session, banner_id=banner_id, image=image
    )


@banner_router.delete(
    "/{banner_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить баннер"
)
async def delete_banner(
    banner_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> None:
    """
    Удалить баннер.

    Требует прав администратора.
    """
    await banners_service.delete_banner(session=session, banner_id=banner_id)
