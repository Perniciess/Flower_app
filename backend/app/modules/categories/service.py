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
    CategoryNotExistsError,
    CategoryParentNotFoundError,
)

from . import repository as category_repository
from .model import Category
from .schema import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
    CategoryWithChildren,
)


async def create_category(
    session: AsyncSession, category_data: CategoryCreate
) -> CategoryResponse:
    category_exist = await category_repository.get_category_by_slug(
        session=session, slug=category_data.slug
    )
    if category_exist is not None:
        raise CategoryAlreadyExistsError(slug=category_data.slug)

    if category_data.parent_id:
        parent = await category_repository.get_category_by_id(
            session=session, category_id=category_data.parent_id
        )
        if not parent:
            raise CategoryParentNotFoundError(parent_id=category_data.parent_id)

    category = await category_repository.create_category(
        session=session, category_data=category_data
    )
    return CategoryResponse.model_validate(category)


async def get_category_by_id(
    session: AsyncSession, category_id: int
) -> CategoryResponse:
    category = await category_repository.get_category_by_id(session, category_id)
    if not category:
        raise CategoryNotExistsError(category_id=category_id)
    return CategoryResponse.model_validate(category)


async def get_category_by_slug(session: AsyncSession, slug: str) -> CategoryResponse:
    category = await category_repository.get_category_by_slug(
        session=session, slug=slug
    )
    if category is None:
        raise CategoryNotExistsError(slug=slug)

    return CategoryResponse.model_validate(category)


async def update_category(
    session: AsyncSession, category_id: int, category_data: CategoryUpdate
) -> CategoryResponse:
    category = await category_repository.get_category_by_id(session, category_id)
    if not category:
        raise CategoryNotExistsError(category_id=category_id)

    if category_data.slug and category_data.slug != category.slug:
        existing = await category_repository.get_category_by_slug(
            session, category_data.slug
        )
        if existing:
            raise CategoryAlreadyExistsError(slug=category_data.slug)

    if category_data.parent_id is not None:
        parent = await category_repository.get_category_by_id(
            session, category_data.parent_id
        )
        if not parent:
            raise CategoryParentNotFoundError(parent_id=category_data.parent_id)

        has_cycle = await _check_circular_dependency(
            session, category_id, category_data.parent_id
        )
        if has_cycle:
            raise ValueError(
                f"Циклическая зависимость: категория {category_id} "
                f"не может быть дочерней для {category_data.parent_id}"
            )

    updated_category = await category_repository.update_category(
        session=session, category_id=category_id, category_data=category_data
    )

    if not updated_category:
        raise CategoryNotExistsError(category_id=category_id)

    return CategoryResponse.model_validate(updated_category)


async def get_all_active_categories(
    session: AsyncSession,
) -> Sequence[CategoryResponse]:
    categories = await category_repository.get_all_active_categories(session=session)
    return [CategoryResponse.model_validate(category) for category in categories]


async def get_all_categories(session: AsyncSession) -> Page[CategoryResponse]:
    query = category_repository.get_categories_query()
    return await paginate(session, query)


async def get_category_tree(
    session: AsyncSession, only_active: bool = True
) -> list[CategoryWithChildren]:
    root_categories = await category_repository.get_root_categories(
        session=session, only_active=only_active
    )

    async def build_tree(category: Category) -> CategoryWithChildren:
        children = await category_repository.get_children(
            session=session, parent_id=category.id, only_active=only_active
        )

        children_tree = [await build_tree(child) for child in children]

        category_dict = CategoryResponse.model_validate(category).model_dump()
        category_dict["children"] = children_tree
        return CategoryWithChildren(**category_dict)

    return [await build_tree(cat) for cat in root_categories]


async def delete_category_by_id(session: AsyncSession, category_id: int) -> bool:
    category = await category_repository.get_category_by_id(session, category_id)
    if not category:
        raise CategoryNotExistsError(category_id=category_id)

    if category.image_url:
        filename = Path(category.image_url).name
        file_path = settings.CATEGORY_UPLOAD_DIR / filename
        if file_path.exists():
            file_path.unlink()

    deleted = await category_repository.delete_category(
        session=session, category_id=category_id
    )
    if not deleted:
        raise CategoryNotExistsError(category_id=category_id)

    return True


async def upload_image(
    *, session: AsyncSession, category_id: int, image: UploadFile
) -> CategoryResponse:
    category = await category_repository.get_category_by_id(session, category_id)
    if not category:
        raise CategoryNotExistsError(category_id=category_id)

    if not image.filename:
        raise ValueError("Файл без имени")

    if category.image_url:
        old_filename = Path(category.image_url).name
        old_path = settings.CATEGORY_UPLOAD_DIR / old_filename
        if old_path.exists():
            old_path.unlink()

    settings.CATEGORY_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    ext = Path(image.filename).suffix
    filename = f"{uuid.uuid4()}{ext}"
    file_path = settings.CATEGORY_UPLOAD_DIR / filename

    content = await image.read()
    async with await anyio.open_file(file_path, "wb") as f:
        await f.write(content)

    url = f"/static/uploads/categories/{filename}"
    category.image_url = url
    await session.flush()

    return CategoryResponse.model_validate(category)


async def _check_circular_dependency(
    session: AsyncSession, category_id: int, parent_id: int
) -> bool:
    if category_id == parent_id:
        return True

    current_id = parent_id
    visited = {category_id}

    while current_id is not None:
        if current_id in visited:
            return True

        visited.add(current_id)

        parent = await category_repository.get_category_by_id(session, current_id)
        if not parent:
            break

        current_id = parent.parent_id

    return False
