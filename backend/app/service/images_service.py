import uuid
from collections.abc import Sequence

import anyio
from fastapi import UploadFile
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import ImageNotFoundError, ImageNotUpdatedError
from app.core.security import get_content_hash
from app.repository import images_repository
from app.schemas.image_schema import ImageCreate, ImageResponse, ImageUpdate
from app.utils.validators.image import validate_image


async def create_image(
    *, session: AsyncSession, image: UploadFile, type: str
) -> ImageResponse:
    ext = validate_image(image)
    filename = f"{uuid.uuid4()}{ext}"

    match type:
        case settings.BANNERS:
            file_path = settings.BANNER_UPLOAD_DIR / filename
            url = settings.get_banner_image_url(filename)
        case settings.PRODUCTS:
            file_path = settings.PRODUCT_UPLOAD_DIR / filename
            url = settings.get_product_image_url(filename)
        case settings.CATEGORIES:
            file_path = settings.CATEGORY_UPLOAD_DIR / filename
            url = settings.get_category_image_url(filename)
        case settings.ADVICES:
            file_path = settings.ADVICE_UPLOAD_DIR / filename
            url = settings.get_advice_image_url(filename)
        case _:
            file_path = settings.SHARED_UPLOAD_DIR / filename
            url = settings.get_shared_image_url(filename)

    content = await image.read()
    file_hash = await get_content_hash(content)
    existing = await images_repository.get_image_by_hash(
        session=session, hash=file_hash
    )
    if existing:
        return ImageResponse.model_validate(existing)

    file_path.parent.mkdir(parents=True, exist_ok=True)
    async with await anyio.open_file(file_path, "wb") as f:
        await f.write(content)

    image_data = ImageCreate(
        path=url,
        hash=file_hash,
        original_filename=filename,
    )

    img = await images_repository.create_image(session=session, image_data=image_data)
    return ImageResponse.model_validate(img)


async def get_images(*, session: AsyncSession) -> Sequence[ImageResponse]:
    images = await images_repository.get_images(session=session)
    return [ImageResponse.model_validate(img) for img in images]


async def get_images_query(*, session: AsyncSession) -> Page[ImageResponse]:
    query = images_repository.get_images_query()
    return await paginate(session, query)


async def update_image(
    *, session: AsyncSession, image_id: int, image_data: ImageUpdate
) -> ImageResponse:
    updated = await images_repository.update_image(
        session=session, image_id=image_id, image_data=image_data
    )
    if updated is None:
        raise ImageNotUpdatedError(image_id=image_id)
    return ImageResponse.model_validate(updated)


async def delete_image(*, session: AsyncSession, image_id: int) -> None:
    existing = await images_repository.get_image(session=session, image_id=image_id)
    if not existing:
        raise ImageNotFoundError(image_id=image_id)

    deleted = await images_repository.delete_image(session=session, image_id=image_id)
    if not deleted:
        raise ImageNotFoundError(image_id=image_id)


async def delete_image_if_orphan(*, session: AsyncSession, image_id: int) -> bool:
    is_used = await images_repository.is_image_referenced(
        session=session, image_id=image_id
    )
    if is_used:
        return False
    image = await images_repository.get_image(session=session, image_id=image_id)
    if image:
        file_path = anyio.Path(image.path.lstrip("/"))
        if await file_path.exists():
            await file_path.unlink()
        await images_repository.delete_image(session=session, image_id=image_id)
    return True
