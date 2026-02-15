from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request, UploadFile, status
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_admin
from app.core.limiter import limiter
from app.db.session import get_db
from app.models.users_model import User
from app.schemas.advices_schema import AdviceCreate, AdviceResponse, AdviceUpdate
from app.service import advices_service

advice_router = APIRouter(prefix="/advices", tags=["advices"])


@advice_router.post(
    "",
    response_model=AdviceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать совет",
)
async def create_advice(
    data: Annotated[AdviceCreate, Form()],
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
    image: UploadFile | None = None,
) -> AdviceResponse:
    """
    Создать совет

    Требует прав администратора
    """

    return await advices_service.create_advice(
        session=session, advice_data=data, image=image
    )


@advice_router.get(
    "",
    response_model=Page[AdviceResponse],
    status_code=status.HTTP_200_OK,
    summary="Получить список активных советов",
)
@limiter.limit("60/minute")
async def get_advices(
    request: Request,
    only_active: bool = True,
    session: AsyncSession = Depends(get_db),
) -> Page[AdviceResponse]:
    """
    Получить список активных советов.
    """
    return await advices_service.get_advices(session=session, only_active=only_active)


@advice_router.get(
    "/all",
    response_model=Page[AdviceResponse],
    status_code=status.HTTP_200_OK,
    summary="Получить список всех советов",
)
async def get_all_advices(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> Page[AdviceResponse]:
    """
    Получить список всех советов.

    Требует прав администратора.
    """
    return await advices_service.get_advices(session=session, only_active=False)


@advice_router.get(
    "/{advice_id}",
    response_model=AdviceResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить совет",
)
async def get_advice(
    advice_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> AdviceResponse:
    """
    Получить совет.

    Требует прав администратора.
    """
    return await advices_service.get_advice(session=session, advice_id=advice_id)


@advice_router.patch(
    "/{advice_id}",
    response_model=AdviceResponse,
    status_code=status.HTTP_200_OK,
    summary="Обновить совет",
)
async def update_advice(
    advice_id: int,
    advice_data: Annotated[AdviceUpdate, Form()],
    image: UploadFile | None = None,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> AdviceResponse:
    """
    Изменить данные совета.

    Требует прав администратора.
    """
    return await advices_service.update_advice(
        session=session, advice_id=advice_id, advice_data=advice_data, image=image
    )


@advice_router.post(
    "/{advice_id}/image",
    response_model=AdviceResponse,
    status_code=status.HTTP_200_OK,
    summary="Загрузить изображение совета",
)
async def upload_advice_image(
    advice_id: int,
    image: UploadFile,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> AdviceResponse:
    """
    Загрузить изображение совета.

    Требует прав администратора.
    """
    return await advices_service.upload_image(
        session=session, advice_id=advice_id, image=image
    )


@advice_router.delete(
    "/{advice_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить совет"
)
async def delete_advice(
    advice_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> None:
    """
    Удалить совет.

    Требует прав администратора.
    """
    await advices_service.delete_advice(session=session, advice_id=advice_id)
