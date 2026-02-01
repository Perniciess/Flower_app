from collections.abc import Sequence

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.favourites_model import Favourite
from app.models.products_model import Product


async def add_to_favourite(*, session: AsyncSession, product_id: int, user_id: int) -> Favourite:
    statement = Favourite(product_id=product_id, user_id=user_id)
    session.add(statement)
    await session.flush()
    return statement


async def delete_from_favourite(*, session: AsyncSession, product_id: int, user_id: int) -> bool:
    statement = (
        delete(Favourite)
        .where(Favourite.product_id == product_id)
        .where(Favourite.user_id == user_id)
        .returning(Favourite.id)
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none() is not None


async def get_favourite_list(*, session: AsyncSession, user_id: int) -> Sequence[Favourite]:
    statement = (
        select(Favourite)
        .where(Favourite.user_id == user_id)
        .options(selectinload(Favourite.product).selectinload(Product.images))
        .order_by(Favourite.id.desc())
    )
    result = await session.execute(statement)
    return result.scalars().all()


async def get_favourite_by_product(*, session: AsyncSession, user_id: int, product_id: int) -> Favourite | None:
    statement = select(Favourite).where(Favourite.user_id == user_id).where(Favourite.product_id == product_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()
