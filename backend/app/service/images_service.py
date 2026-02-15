import uuid

import anyio
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import get_file_hash
from app.repository import images_repository
from app.schemas.image_schema import ImageCreate, ImageResponse
from app.utils.validators.image import validate_image


async def create_image(
    *, session: AsyncSession, image: UploadFile, type: str
) -> ImageResponse:
    ext = validate_image(image)
    filename = f"{uuid.uuid4()}{ext}"

    match type:
        case "banners":
            file_path = settings.BANNER_UPLOAD_DIR / filename
            url = settings.get_banner_image_url(filename)
        case "products":
            file_path = settings.PRODUCT_UPLOAD_DIR / filename
            url = settings.get_product_image_url(filename)
        case "categories":
            file_path = settings.CATEGORY_UPLOAD_DIR / filename
            url = settings.get_category_image_url(filename)
        case "advices":
            file_path = settings.ADVICE_UPLOAD_DIR / filename
            url = settings.get_advice_image_url(filename)
        case _:
            file_path = settings.SHARED_UPLOAD_DIR / filename
            url = settings.get_shared_image_url(filename)

    content = await image.read()
    async with await anyio.open_file(file_path, "wb") as f:
        await f.write(content)

    hash = await get_file_hash(str(file_path))

    image_data = ImageCreate(
        path=url,
        hash=hash,
        original_filename=filename,
    )

    img = await images_repository.create_image(session=session, image_data=image_data)
    return ImageResponse.model_validate(img)
