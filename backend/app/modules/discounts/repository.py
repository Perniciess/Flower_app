from collections.abc import Sequence

from sqlalchemy import Select, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .model import Discount
from .schema import DiscountCreate, DiscountUpdate


async def create_discount(*, session: AsyncSession, discount_data: DiscountCreate) -> Discount:
    discount = Discount(**discount_data.model_dump())
    session.add(discount)
    await session.flush()
    return discount


async def get_discount(*, session: AsyncSession, discount_id: int) -> Discount | None:
    statement = select(Discount).where(Discount.id == discount_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


def get_discounts_query() -> Select[tuple[Discount]]:
    return select(Discount).order_by(Discount.id)


async def update_discount(*, session: AsyncSession, discount_id: int, discount_data: DiscountUpdate) -> Discount | None:
    statement = (
        update(Discount).where(Discount.id == discount_id).values(**discount_data.model_dump(exclude_unset=True)).returning(Discount)
    )
    result = await session.execute(statement)
    await session.flush()
    return result.scalar_one_or_none()


async def delete_discount(*, session: AsyncSession, discount_id: int) -> bool:
    statement = delete(Discount).where(Discount.id == discount_id).returning(Discount.id)
    result = await session.execute(statement)
    return result.scalar_one_or_none() is not None


async def get_active_for_product(*, session: AsyncSession, product_id: int) -> Discount | None:
    statement = select(Discount).where(
        Discount.product_id == product_id,
        Discount.is_active.is_(True),
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def get_active_for_category_ids(*, session: AsyncSession, category_ids: Sequence[int]) -> Sequence[Discount]:
    if not category_ids:
        return []
    statement = select(Discount).where(
        Discount.category_id.in_(category_ids),
        Discount.is_active.is_(True),
    )
    result = await session.execute(statement)
    return result.scalars().all()


async def get_active_for_products(*, session: AsyncSession, product_ids: Sequence[int]) -> Sequence[Discount]:
    if not product_ids:
        return []
    statement = select(Discount).where(
        Discount.product_id.in_(product_ids),
        Discount.is_active.is_(True),
    )
    result = await session.execute(statement)
    return result.scalars().all()
