from sqlalchemy import Select, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.advices_model import Advice
from app.schemas.advices_schema import AdviceCreate, AdviceUpdate


async def create_advice(*, session: AsyncSession, advice_data: AdviceCreate) -> Advice:
    advice = Advice(**advice_data.model_dump())
    session.add(advice)
    await session.flush()
    return advice


def get_advices_query(*, only_active: bool = False) -> Select[tuple[Advice]]:
    statement = select(Advice).order_by(Advice.sort_order, Advice.id)
    if only_active:
        statement = statement.where(Advice.is_active)
    return statement


async def update_advice(
    *, session: AsyncSession, advice_id: int, advice_data: AdviceUpdate
) -> Advice | None:
    statement = (
        update(Advice)
        .where(Advice.id == advice_id)
        .values(**advice_data.model_dump(exclude_unset=True))
        .returning(Advice)
    )
    result = await session.execute(statement)
    await session.flush()
    return result.scalar_one_or_none()


async def update_advice_image(
    *, session: AsyncSession, advice_id: int, image_url: str
) -> Advice | None:
    statement = (
        update(Advice)
        .where(Advice.id == advice_id)
        .values(image_url=image_url)
        .returning(Advice)
    )
    result = await session.execute(statement)
    await session.flush()
    return result.scalar_one_or_none()


async def delete_advice(*, session: AsyncSession, advice_id: int) -> str | None:
    statement = delete(Advice).where(Advice.id == advice_id).returning(Advice.image_url)
    result = await session.execute(statement)
    return result.scalar_one_or_none()
