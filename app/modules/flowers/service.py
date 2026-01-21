from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from . import repository as flower_repository
from .schema import FlowerCreate, FlowerResponse


async def create_flower(*, session: AsyncSession, flower_data: FlowerCreate) -> FlowerResponse:
    flower = await flower_repository.create_flower(session=session, data=flower_data.model_dump())
    return FlowerResponse.model_validate(flower)


async def get_flowers(*, session: AsyncSession) -> Sequence[FlowerResponse]:
    flowers = await flower_repository.get_flowers(session=session)
    return [FlowerResponse.model_validate(flower) for flower in flowers]
