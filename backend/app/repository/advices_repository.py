from collections.abc import Sequence

from sqlalchemy import Select, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.advices_model import Advice
from app.schemas.advices_schema import AdviceCreate, AdviceUpdate


async def create_advice(
    *, session: AsyncSession, advice_data: AdviceCreate, image_id: int | None
) -> Advice:
    advice = Advice(**advice_data.model_dump(), image_id=image_id)
    session.add(advice)
    await session.flush()
    return advice


async def get_advice(*, session: AsyncSession, advice_id: int) -> Advice | None:
    statement = select(Advice).where(Advice.id == advice_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def get_advices(
    *, session: AsyncSession, only_active: bool = False
) -> Sequence[Advice]:
    statement = select(Advice).order_by(Advice.sort_order, Advice.id)
    if only_active:
        statement = statement.where(Advice.is_active)
    result = await session.execute(statement)
    return result.scalars().all()


def get_advices_query(*, only_active: bool = False) -> Select[tuple[Advice]]:
    statement = select(Advice).order_by(Advice.sort_order, Advice.id)
    if only_active:
        statement = statement.where(Advice.is_active)
    return statement


async def update_advice(
    *,
    session: AsyncSession,
    advice_id: int,
    advice_data: AdviceUpdate,
    image_id: int | None = None,
) -> Advice | None:
    update_data = advice_data.model_dump(exclude_unset=True)
    if image_id is not None:
        update_data["image_id"] = image_id
    statement = (
        update(Advice)
        .where(Advice.id == advice_id)
        .values(**update_data)
        .returning(Advice)
    )
    result = await session.execute(statement)
    await session.flush()
    return result.scalar_one_or_none()


async def delete_advice(*, session: AsyncSession, advice_id: int) -> bool:
    statement = delete(Advice).where(Advice.id == advice_id).returning(Advice.id)
    result = await session.execute(statement)
    return result.scalar_one_or_none() is not None


async def set_advice_image(
    *, session: AsyncSession, advice_id: int, image_id: int | None
) -> Advice | None:
    statement = (
        update(Advice)
        .where(Advice.id == advice_id)
        .values(image_id=image_id)
        .returning(Advice)
    )
    result = await session.execute(statement)
    await session.flush()
    return result.scalar_one_or_none()
