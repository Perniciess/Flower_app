from collections.abc import Sequence

from fastapi import APIRouter, Depends, Request, UploadFile, status, Form
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_admin
from app.core.limiter import limiter
from app.db.session import get_db
from app.models.users_model import User
from app.schemas.categories_schema import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
    CategoryWithChildren,
)
from app.service import categories_service

category_router = APIRouter(prefix="/category", tags=["category"])


@category_router.post(
    "/create",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создание категории",
)
async def create_category(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
    name: str = Form(..., min_length=1, max_length=255, description="Название категории"),
    slug: str = Form(..., min_length=1, max_length=255, description="URL-friendly идентификатор категории"),
    description: str | None = Form(default=None, max_length=2000, description="Описание категории"),
    parent_id: int | None = Form(default=None, description="ID родительской категории"),
    sort_order: int = Form(default=0, description="Порядок сортировки"),
    is_active: bool = Form(default=False, description="Статус активности категории"),
    image: UploadFile | None = None,
) -> CategoryResponse:
    """
    Создать категорию.

    Требует прав администратора.
    """
    category_data = CategoryCreate(
        name=name,
        slug=slug,
        description=description,
        parent_id=parent_id,
        sort_order=sort_order,
        is_active=is_active,
    )
    category = await categories_service.create_category(
        session=session, category_data=category_data, image=image
    )
    return category
@category_router.get(
    "/all_active",
    response_model=Sequence[CategoryResponse],
    status_code=status.HTTP_200_OK,
    summary="Получить список всех активных категорий",
)
@limiter.limit("60/minute")
async def get_all_active_categories(
    request: Request,
    session: AsyncSession = Depends(get_db),
) -> Sequence[CategoryResponse]:
    """
    Получить список всех активных.
    """
    categories = await categories_service.get_all_active_categories(session=session)
    return categories


@category_router.get(
    "/all",
    response_model=Page[CategoryResponse],
    status_code=status.HTTP_200_OK,
    summary="Список всех категорий",
)
async def get_all_categories_admin(
    current_user: User = Depends(require_admin),
    session: AsyncSession = Depends(get_db),
) -> Page[CategoryResponse]:
    """
    Получить список всех категорий.

    Требует прав администратора.
    """
    categories = await categories_service.get_all_categories(session=session)
    return categories


@category_router.get(
    "/tree",
    response_model=list[CategoryWithChildren],
    status_code=status.HTTP_200_OK,
    summary="Получить дерево категорий",
)
@limiter.limit("60/minute")
async def get_category_tree(
    request: Request,
    session: AsyncSession = Depends(get_db),
    only_active: bool = True,
) -> list[CategoryWithChildren]:
    """
    Получить дерево категорий.
    """
    return await categories_service.get_category_tree(
        session=session, only_active=only_active
    )


@category_router.get(
    "/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить категорию по ID",
)
@limiter.limit("60/minute")
async def get_category_by_id(
    request: Request, category_id: int, session: AsyncSession = Depends(get_db)
) -> CategoryResponse:
    """
    Получить категорию по ID.
    """
    return await categories_service.get_category_by_id(
        session=session, category_id=category_id
    )


@category_router.patch(
    "/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Обновить категорию",
)
async def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> CategoryResponse:
    """
    Обновить данные в категории.

    Требует прав администратора.
    """
    return await categories_service.update_category(
        session=session, category_id=category_id, category_data=category_data
    )


@category_router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить категорию",
)
async def delete_category_by_id(
    category_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> None:
    """
    Удаление категории.

    Требует прав администратора.
    """
    await categories_service.delete_category_by_id(
        session=session, category_id=category_id
    )


@category_router.post(
    "/{category_id}/image",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Загрузить изображение категории",
)
async def upload_category_image(
    category_id: int,
    image: UploadFile,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> CategoryResponse:
    """
    Загрузка изображения категории.

    Требует прав администратора.
    """
    category = await categories_service.upload_image(
        session=session, category_id=category_id, image=image
    )
    return category


@category_router.delete(
    "/{category_id}/image",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Удалить изображение категории",
)
async def delete_category_image(
    category_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> CategoryResponse:
    """
    Удаление изображение категории.

    Требует прав администратора.
    """
    return await categories_service.delete_image(
        session=session, category_id=category_id
    )


@category_router.get(
    "/{slug}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить категорию по slug",
)
@limiter.limit("60/minute")
async def get_category_by_slug(
    request: Request, slug: str, session: AsyncSession = Depends(get_db)
) -> CategoryResponse:
    """
    Получить категорию по slug.
    """
    category = await categories_service.get_category_by_slug(session=session, slug=slug)
    return category
