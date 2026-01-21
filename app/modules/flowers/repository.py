from collections.abc import Mapping, Sequence
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .model import Flower


async def create_flower(*, session: AsyncSession, data: Mapping[str, Any]) -> Flower:
    flower = Flower(name=data["name"], price=data["price"], description=data["description"], color=data["color"])
    session.add(flower)
    await session.flush()
    return flower


async def get_flowers(*, session: AsyncSession) -> Sequence[Flower]:
    statement = select(Flower).order_by(Flower.id)
    flowers = await session.execute(statement)
    return flowers.scalars().all()
