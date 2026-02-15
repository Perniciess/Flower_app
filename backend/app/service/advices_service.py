from fastapi import UploadFile
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import AdviceNotFoundError
from app.repository import advices_repository
from app.schemas.advices_schema import AdviceCreate, AdviceResponse, AdviceUpdate

from . import images_service


async def create_advice(
    *, session: AsyncSession, advice_data: AdviceCreate, image: UploadFile | None = None
) -> AdviceResponse:
    image_id = None
    if image:
        img = await images_service.create_image(
            session=session, image=image, type=settings.ADVICES
        )
        image_id = img.id
    advice = await advices_repository.create_advice(
        session=session, advice_data=advice_data, image_id=image_id
    )
    return AdviceResponse.model_validate(advice)


async def get_advice(*, session: AsyncSession, advice_id: int) -> AdviceResponse:
    advice = await advices_repository.get_advice(session=session, advice_id=advice_id)
    if advice is None:
        raise AdviceNotFoundError(advice_id=advice_id)
    return AdviceResponse.model_validate(advice)


async def get_advices(
    *, session: AsyncSession, only_active: bool = False
) -> Page[AdviceResponse]:
    query = advices_repository.get_advices_query(only_active=only_active)
    return await paginate(session, query)


async def update_advice(
    *,
    session: AsyncSession,
    advice_id: int,
    advice_data: AdviceUpdate,
    image: UploadFile | None = None,
) -> AdviceResponse:
    image_id = None
    if image:
        img = await images_service.create_image(
            session=session, image=image, type=settings.ADVICES
        )
        image_id = img.id
    advice = await advices_repository.update_advice(
        session=session, advice_id=advice_id, advice_data=advice_data, image_id=image_id
    )
    if not advice:
        raise AdviceNotFoundError(advice_id)
    return AdviceResponse.model_validate(advice)


async def upload_image(
    *, session: AsyncSession, advice_id: int, image: UploadFile
) -> AdviceResponse:
    advice = await advices_repository.get_advice(session=session, advice_id=advice_id)
    if not advice:
        raise AdviceNotFoundError(advice_id=advice_id)
    img = await images_service.create_image(
        session=session, image=image, type=settings.ADVICES
    )
    updated = await advices_repository.set_advice_image(
        session=session, advice_id=advice_id, image_id=img.id
    )
    return AdviceResponse.model_validate(updated)


async def delete_advice(*, session: AsyncSession, advice_id: int) -> bool:
    deleted = await advices_repository.delete_advice(
        session=session, advice_id=advice_id
    )
    if not deleted:
        raise AdviceNotFoundError(advice_id=advice_id)
    return True
