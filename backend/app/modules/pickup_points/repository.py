from collections.abc import Sequence

from sqlalchemy import Select, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.pickup_points.model import PickupPoint
from app.modules.pickup_points.schema import PickupPointCreate, PickupPointUpdate


async def create_pickup_point(session: AsyncSession, data: PickupPointCreate) -> PickupPoint:
    pickup_point = PickupPoint(**data.model_dump())
    session.add(pickup_point)
    await session.commit()
    await session.refresh(pickup_point)
    return pickup_point


async def get_pickup_point_by_id(session: AsyncSession, pickup_point_id: int) -> PickupPoint | None:
    result = await session.execute(select(PickupPoint).where(PickupPoint.id == pickup_point_id))
    return result.scalar_one_or_none()


async def get_all_active_pickup_points(session: AsyncSession) -> Sequence[PickupPoint]:
    result = await session.execute(
        select(PickupPoint).where(PickupPoint.is_active).order_by(PickupPoint.sort_order, PickupPoint.name)
    )
    return list(result.scalars().all())


def get_all_pickup_points_query() -> Select[tuple[PickupPoint]]:
    return select(PickupPoint).order_by(PickupPoint.sort_order, PickupPoint.name)


async def update_pickup_point(session: AsyncSession, pickup_point: PickupPoint, data: PickupPointUpdate) -> PickupPoint:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(pickup_point, field, value)

    await session.commit()
    await session.refresh(pickup_point)
    return pickup_point


async def delete_pickup_point(session: AsyncSession, pickup_point_id: int) -> bool:
    statement = delete(PickupPoint).where(PickupPoint.id == pickup_point_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none() is not None
