import uuid

import anyio
from fastapi import UploadFile
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import BannerNotFoundError
from app.repository import banners_repository
from app.schemas.banners_schema import BannerCreate, BannerResponse, BannerUpdate
from app.utils.validators.image import validate_image


async def create_banner(
    *, session: AsyncSession, banner_data: BannerCreate, image: UploadFile | None = None
) -> BannerResponse:
    banner = await banners_repository.create_banner(
        session=session, banner_data=banner_data
    )

    if image is not None:
        ext = validate_image(image)
        settings.BANNER_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        filename = f"{uuid.uuid4()}{ext}"
        file_path = settings.BANNER_UPLOAD_DIR / filename

        content = await image.read()
        async with await anyio.open_file(file_path, "wb") as f:
            await f.write(content)

        url = settings.get_banner_image_url(filename)
        banner = await banners_repository.update_banner_image(
            session=session, banner_id=banner.id, image_url=url
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
    *, session: AsyncSession, banner_id: int, banner_data: BannerUpdate
) -> BannerResponse:
    banner = await banners_repository.update_banner(
        session=session, banner_id=banner_id, banner_data=banner_data
    )
    if banner is None:
        raise BannerNotFoundError(banner_id=banner_id)
    return BannerResponse.model_validate(banner)


async def upload_image(
    *, session: AsyncSession, banner_id: int, image: UploadFile
) -> BannerResponse:
    existing = await banners_repository.get_banner(session=session, banner_id=banner_id)
    if existing is None:
        raise BannerNotFoundError(banner_id=banner_id)

    if existing.image_url:
        old_path = (settings.ROOT_DIR / existing.image_url.lstrip("/")).resolve()
        if (
            str(old_path).startswith(str(settings.BANNER_UPLOAD_DIR.resolve()))
            and old_path.exists()
        ):
            old_path.unlink()

    ext = validate_image(image)
    settings.BANNER_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid.uuid4()}{ext}"
    file_path = settings.BANNER_UPLOAD_DIR / filename

    content = await image.read()
    async with await anyio.open_file(file_path, "wb") as f:
        await f.write(content)

    url = settings.get_banner_image_url(filename)
    banner = await banners_repository.update_banner_image(
        session=session, banner_id=banner_id, image_url=url
    )
    return BannerResponse.model_validate(banner)


async def delete_banner(*, session: AsyncSession, banner_id: int) -> bool:
    image_url = await banners_repository.delete_banner(
        session=session, banner_id=banner_id
    )
    if image_url is None:
        raise BannerNotFoundError(banner_id=banner_id)

    if image_url:
        file_path = (settings.ROOT_DIR / image_url.lstrip("/")).resolve()
        if (
            str(file_path).startswith(str(settings.BANNER_UPLOAD_DIR.resolve()))
            and file_path.exists()
        ):
            file_path.unlink()

    return True
