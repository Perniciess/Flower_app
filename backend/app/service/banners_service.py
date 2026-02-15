from fastapi import UploadFile
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import BannerNotFoundError
from app.repository import banners_repository
from app.schemas.banners_schema import BannerCreate, BannerResponse, BannerUpdate

from . import images_service


async def create_banner(
    *, session: AsyncSession, banner_data: BannerCreate, image: UploadFile | None = None
) -> BannerResponse:
    image_id = None
    if image:
        img = await images_service.create_image(
            session=session, image=image, type=settings.BANNERS
        )
        image_id = img.id
    banner = await banners_repository.create_banner(
        session=session, banner_data=banner_data, image_id=image_id
    )
    return BannerResponse.model_validate(banner)


async def get_banner(*, session: AsyncSession, banner_id: int) -> BannerResponse:
    banner = await banners_repository.get_banner(session=session, banner_id=banner_id)
    if banner is None:
        raise BannerNotFoundError(banner_id=banner_id)
    return BannerResponse.model_validate(banner)


async def get_banners(
    *, session: AsyncSession, only_active: bool = False
) -> Page[BannerResponse]:
    query = banners_repository.get_banners_query(only_active=only_active)
    return await paginate(session, query)


async def update_banner(
    *,
    session: AsyncSession,
    banner_id: int,
    banner_data: BannerUpdate,
    image: UploadFile | None = None,
) -> BannerResponse:
    image_id = None
    if image:
        img = await images_service.create_image(
            session=session, image=image, type=settings.BANNERS
        )
        image_id = img.id
    banner = await banners_repository.update_banner(
        session=session, banner_id=banner_id, banner_data=banner_data, image_id=image_id
    )
    if not banner:
        raise BannerNotFoundError(banner_id)
    return BannerResponse.model_validate(banner)


async def upload_image(
    *, session: AsyncSession, banner_id: int, image: UploadFile
) -> BannerResponse:
    banner = await banners_repository.get_banner(session=session, banner_id=banner_id)
    if not banner:
        raise BannerNotFoundError(banner_id=banner_id)
    img = await images_service.create_image(
        session=session, image=image, type=settings.BANNERS
    )
    updated = await banners_repository.set_banner_image(
        session=session, banner_id=banner_id, image_id=img.id
    )
    return BannerResponse.model_validate(updated)


async def delete_banner(*, session: AsyncSession, banner_id: int) -> bool:
    deleted = await banners_repository.delete_banner(
        session=session, banner_id=banner_id
    )
    if not deleted:
        raise BannerNotFoundError(banner_id=banner_id)
    return True
