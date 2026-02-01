import uuid
from collections.abc import Sequence
from pathlib import Path

import anyio
from fastapi import UploadFile
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import (
    CategoryAlreadyExistsError,
    CategoryCycleError,
    CategoryNotExistsError,
    CategoryParentNotFoundError,
)
from app.models.categories_model import Category
from app.repository import categories_repository
from app.schemas.categories_schema import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
    CategoryWithChildren,
)
from app.utils.validators.image import validate_image


async def create_category(session: AsyncSession, category_data: CategoryCreate) -> CategoryResponse:
    """
    Создает новую категорию в базе данных.

    Args:
        session: сессия базы данных
        category_data: данные для создания категории

    Returns:
        CategoryResponse с данными созданной категории

    Raises:
        CategoryAlreadyExistsError: если категория уже существует
        CategoryParentNotFoundError: если заданная родительская категория не существует
    """
    category_exist = await categories_repository.get_category_by_slug(session=session, slug=category_data.slug)
    if category_exist is not None:
        raise CategoryAlreadyExistsError(slug=category_data.slug)

    if category_data.parent_id:
        parent = await categories_repository.get_category_by_id(session=session, category_id=category_data.parent_id)
        if not parent:
            raise CategoryParentNotFoundError(parent_id=category_data.parent_id)

    category = await categories_repository.create_category(session=session, category_data=category_data)
    return CategoryResponse.model_validate(category)


async def get_category_by_id(session: AsyncSession, category_id: int) -> CategoryResponse:
    """
    Возвращает категорию по ID из базы данных.

    Args:
        session: сессия базы данных
        category_id: идентификатор категории

    Returns:
        CategoryResponse с данными созданной категории

    Raises:
        CategoryNotExistsError: если категория не существует
    """
    category = await categories_repository.get_category_by_id(session, category_id)
    if not category:
        raise CategoryNotExistsError(category_id=category_id)
    return CategoryResponse.model_validate(category)


async def get_category_by_slug(session: AsyncSession, slug: str) -> CategoryResponse:
    """
    Возвращает категорию по slug из базы данных.

    Args:
        session: сессия базы данных
        slug: slug категории

    Returns:
        CategoryResponse с данными созданной категории

    Raises:
        CategoryNotExistsError: если категория не существует
    """
    category = await categories_repository.get_category_by_slug(session=session, slug=slug)
    if category is None:
        raise CategoryNotExistsError(slug=slug)

    return CategoryResponse.model_validate(category)


async def update_category(session: AsyncSession, category_id: int, category_data: CategoryUpdate) -> CategoryResponse:
    """
    Обновляет информацию о категории в базе данных.

    Args:
        session: сессия базы данных
        category_id: идентификатор категории
        category_data: новые данные категории

    Returns:
        CategoryResponse с данными обновленной категории

    Raises:
        CategoryNotExistsError: если категория не существует
        CategoryAlreadyExistsError: когда категории задается новый slug, но категория с таким slug уже существует
        CategoryParentNotFoundError: если задается новая родительская категория, которой не существует
        CategoryCycleError: если родительская и дочерняя категории создают циклическую зависимость
    """
    category = await categories_repository.get_category_by_id(session, category_id)
    if not category:
        raise CategoryNotExistsError(category_id=category_id)

    if category_data.slug and category_data.slug != category.slug:
        existing = await categories_repository.get_category_by_slug(session, category_data.slug)
        if existing:
            raise CategoryAlreadyExistsError(slug=category_data.slug)

    if category_data.parent_id is not None:
        parent = await categories_repository.get_category_by_id(session, category_data.parent_id)
        if not parent:
            raise CategoryParentNotFoundError(parent_id=category_data.parent_id)

        has_cycle = await _check_circular_dependency(session, category_id, category_data.parent_id)
        if has_cycle:
            raise CategoryCycleError(category_id=category_id, parent_id=category_data.parent_id)

    updated_category = await categories_repository.update_category(
        session=session, category_id=category_id, category_data=category_data
    )

    if not updated_category:
        raise CategoryNotExistsError(category_id=category_id)

    return CategoryResponse.model_validate(updated_category)


async def get_all_active_categories(
    session: AsyncSession,
) -> Sequence[CategoryResponse]:
    """
    Возвращает список всех активных категорий.

    Args:
        session: сессия базы данных

    Returns:
        Sequence[CategoryResponse] список с данными активных категорий
    """
    categories = await categories_repository.get_all_active_categories(session=session)
    return [CategoryResponse.model_validate(category) for category in categories]


async def get_all_categories(session: AsyncSession) -> Page[CategoryResponse]:
    """
    Возвращает пагинированный список всех категорий.

    Args:
        session: сессия базы данных

    Returns:
        Page[CategoryResponse] с пагинированным списком категорий
    """
    query = categories_repository.get_categories_query()
    return await paginate(session, query)


async def get_category_tree(session: AsyncSession, only_active: bool = True) -> list[CategoryWithChildren]:
    """
    Возвращает дерево категорий, рекурсивно собирая дочерние элементы.

    Args:
        session: сессия базы данных
        only_active: если True, возвращает только активные категории

    Returns:
        CategoryWithChildren список корневых категорий с вложенными дочерними элементами
    """
    root_categories = await categories_repository.get_root_categories(session=session, only_active=only_active)

    async def build_tree(category: Category) -> CategoryWithChildren:
        children = await categories_repository.get_children(
            session=session, parent_id=category.id, only_active=only_active
        )

        children_tree = [await build_tree(child) for child in children]

        category_dict = CategoryResponse.model_validate(category).model_dump()
        category_dict["children"] = children_tree
        return CategoryWithChildren(**category_dict)

    return [await build_tree(cat) for cat in root_categories]


async def delete_category_by_id(session: AsyncSession, category_id: int) -> None:
    """
    Удаляет категорию по ID и ее изображение.

    Args:
        session: сессия базы данных
        category_id: идентификатор категории

    Returns:
        None

    Raises:
        CategoryNotExistsError: если категория не существует
    """
    category = await categories_repository.get_category_by_id(session, category_id)
    if not category:
        raise CategoryNotExistsError(category_id=category_id)

    if category.image_url:
        filename = Path(category.image_url).name
        file_path = settings.CATEGORY_UPLOAD_DIR / filename
        if file_path.exists():
            file_path.unlink()

    deleted = await categories_repository.delete_category(session=session, category_id=category_id)
    if not deleted:
        raise CategoryNotExistsError(category_id=category_id)


async def delete_image(*, session: AsyncSession, category_id: int) -> CategoryResponse:
    """
    Удаляет изображение категории.

    Args:
        session: сессия базы данных
        category_id: идентификатор категории

    Returns:
        CategoryResponse с данными о категории

    Raises:
        CategoryNotExistsError: если категория не существует
    """
    category = await categories_repository.get_category_by_id(session, category_id)
    if not category:
        raise CategoryNotExistsError(category_id=category_id)

    if category.image_url:
        filename = Path(category.image_url).name
        file_path = settings.CATEGORY_UPLOAD_DIR / filename
        if file_path.exists():
            file_path.unlink()

        category.image_url = None
        await session.flush()

    return CategoryResponse.model_validate(category)


async def upload_image(*, session: AsyncSession, category_id: int, image: UploadFile) -> CategoryResponse:
    """
    Загружает изображение категории.

    Args:
        session: сессия базы данных
        category_id: идентификатор категории
        image: файл изображения

    Returns:
        CategoryResponse с данными о категории

    Raises:
        CategoryNotExistsError: если категория не существует
        ValueError: если файл невалидный
    """
    category = await categories_repository.get_category_by_id(session, category_id)
    if not category:
        raise CategoryNotExistsError(category_id=category_id)

    ext = validate_image(image)

    if category.image_url:
        old_filename = Path(category.image_url).name
        old_path = settings.CATEGORY_UPLOAD_DIR / old_filename
        if old_path.exists():
            old_path.unlink()

    settings.CATEGORY_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid.uuid4()}{ext}"
    file_path = settings.CATEGORY_UPLOAD_DIR / filename

    content = await image.read()
    async with await anyio.open_file(file_path, "wb") as f:
        await f.write(content)

    url = f"/static/uploads/categories/{filename}"
    category.image_url = url
    await session.flush()

    return CategoryResponse.model_validate(category)


async def _check_circular_dependency(session: AsyncSession, category_id: int, parent_id: int) -> bool:
    """
    Проверяет наличие циклической зависимости при назначении нового родителя категории.

    Поднимается по цепочке родителей от parent_id вверх. Если на пути встречается
    category_id — значит, назначение создаст цикл.

    Args:
        session: сессия базы данных
        category_id: идентификатор категории, которой назначается новый родитель
        parent_id: идентификатор предполагаемого родителя

    Returns:
        True, если обнаружен цикл, иначе False
    """
    if category_id == parent_id:
        return True

    current_id = parent_id
    visited = {category_id}

    while current_id is not None:
        if current_id in visited:
            return True

        visited.add(current_id)

        parent = await categories_repository.get_category_by_id(session, current_id)
        if not parent:
            break

        current_id = parent.parent_id

    return False
