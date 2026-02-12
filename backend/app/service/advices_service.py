import uuid

import anyio
from fastapi import UploadFile
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.repository import advices_repository
from app.schemas.advices_schema import AdviceCreate, AdviceResponse
from app.utils.validators.image import validate_image


async def create_advice(
    *, session: AsyncSession, advice_data: AdviceCreate, image: UploadFile | None = None
) -> AdviceResponse:
    advice = await advices_repository.create_advice(
        session=session, advice_data=advice_data
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
        advice = await advices_repository.update_advice_image(
            session=session, advice_id=advice.id, image_url=url
        )

    return AdviceResponse.model_validate(advice)


async def get_banners(
    *, session: AsyncSession, only_active: bool = False
) -> Page[AdviceResponse]:
    query = advices_repository.get_advices_query(only_active=only_active)
    return await paginate(session, query)
