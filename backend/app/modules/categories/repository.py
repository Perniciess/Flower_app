from collections.abc import Sequence

from sqlalchemy import Select, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .model import Category
from .schema import CategoryCreate, CategoryUpdate


async def get_category_by_id(session: AsyncSession, category_id: int, with_relations: bool = False) -> Category | None:
    statement = select(Category).where(Category.id == category_id)

    if with_relations:
        statement = statement.options(selectinload(Category.children), selectinload(Category.parent))

    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def get_category_by_slug(session: AsyncSession, slug: str) -> Category | None:
    statement = select(Category).where(Category.slug == slug)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def create_category(session: AsyncSession, category_data: CategoryCreate) -> Category:
    category = Category(**category_data.model_dump())
    session.add(category)
    await session.flush()
    return category


async def update_category(*, session: AsyncSession, category_id: int, category_data: CategoryUpdate) -> Category | None:
    statement = (
        update(Category).where(Category.id == category_id).values(**category_data.model_dump()).returning(Category)
    )

    result = await session.execute(statement)
    await session.flush()
    return result.scalar_one_or_none()


async def get_all_active_categories(
    session: AsyncSession,
) -> Sequence[Category]:
    statement = select(Category).where(Category.is_active).order_by(Category.sort_order, Category.id)
    result = await session.execute(statement)
    return result.scalars().all()


async def get_root_categories(session: AsyncSession, only_active: bool = True) -> Sequence[Category]:
    statement = select(Category).where(Category.parent_id.is_(None))

    if only_active:
        statement = statement.where(Category.is_active)

    statement = statement.order_by(Category.sort_order, Category.id).options(selectinload(Category.children))

    result = await session.execute(statement)
    return result.scalars().all()


async def get_children(session: AsyncSession, parent_id: int, only_active: bool = True) -> Sequence[Category]:
    statement = select(Category).where(Category.parent_id == parent_id)

    if only_active:
        statement = statement.where(Category.is_active)

    statement = statement.order_by(Category.sort_order, Category.id)

    result = await session.execute(statement)
    return result.scalars().all()


def get_categories_query() -> Select[tuple[Category]]:
    return select(Category).order_by(Category.sort_order, Category.id)


async def delete_category(*, session: AsyncSession, category_id: int) -> bool:
    statement = delete(Category).where(Category.id == category_id).returning(Category.id)
    result = await session.execute(statement)
    return result.scalar_one_or_none() is not None
