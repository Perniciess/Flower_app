from collections.abc import Sequence

from fastapi import APIRouter, Depends, UploadFile
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, require_admin
from app.modules.users.model import User

from . import service as category_service
from .schema import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
    CategoryWithChildren,
)

category_router = APIRouter(prefix="/category", tags=["category"])


@category_router.post("/create", response_model=CategoryResponse, summary="Создание категории")
async def create_category(
    category_data: CategoryCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> CategoryResponse:
    """
    Создание категории.

    Требует прав администратора.
    """
    category = await category_service.create_category(session=session, category_data=category_data)
    return category


@category_router.get(
    "/all_active",
    response_model=Sequence[CategoryResponse],
    summary="Получить список всех активных категорий",
)
async def get_all_active_categories(
    session: AsyncSession = Depends(get_db),
) -> Sequence[CategoryResponse]:
    """
    Получить список всех активных.
    """
    categories = await category_service.get_all_active_categories(session=session)
    return categories


@category_router.get(
    "/all",
    response_model=Page[CategoryResponse],
    summary="Список всех категорий",
)
async def get_all_categories_admin(
    current_user: User = Depends(require_admin),
    session: AsyncSession = Depends(get_db),
) -> Page[CategoryResponse]:
    """
    Получение списка всех категорий.

    Требует прав администратора.
    """
    categories = await category_service.get_all_categories(session=session)
    return categories


@category_router.get(
    "/tree",
    response_model=list[CategoryWithChildren],
    summary="Получить дерево категорий",
)
async def get_category_tree(
    session: AsyncSession = Depends(get_db),
    only_active: bool = True,
) -> list[CategoryWithChildren]:
    """
    Получить дерево категорий.
    """
    return await category_service.get_category_tree(session=session, only_active=only_active)


@category_router.get(
    "/{category_id:int}",
    response_model=CategoryResponse,
    summary="Получить категорию по ID",
)
async def get_category_by_id(category_id: int, session: AsyncSession = Depends(get_db)) -> CategoryResponse:
    """
    Получить категорию по ID.
    """
    return await category_service.get_category_by_id(session=session, category_id=category_id)


@category_router.patch(
    "/{category_id:int}",
    response_model=CategoryResponse,
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
    return await category_service.update_category(session=session, category_id=category_id, category_data=category_data)


@category_router.delete("/{category_id:int}", status_code=204, summary="Удалить категорию")
async def delete_category_by_id(
    category_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> None:
    """
    Удаление категории.

    Требует прав администратора.
    """
    await category_service.delete_category_by_id(session=session, category_id=category_id)


@category_router.post(
    "/{category_id:int}/image",
    response_model=CategoryResponse,
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
    category = await category_service.upload_image(session=session, category_id=category_id, image=image)
    return category


@category_router.delete(
    "/{category_id:int}/image",
    response_model=CategoryResponse,
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
    return await category_service.delete_image(session=session, category_id=category_id)


@category_router.get("/{slug}", response_model=CategoryResponse, summary="Получить категорию по slug")
async def get_category_by_slug(slug: str, session: AsyncSession = Depends(get_db)) -> CategoryResponse:
    """
    Получить категорию по slug.
    """
    category = await category_service.get_category_by_slug(session=session, slug=slug)
    return category
