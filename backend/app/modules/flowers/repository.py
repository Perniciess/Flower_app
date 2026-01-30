from collections.abc import Mapping, Sequence
from decimal import Decimal
from typing import Any

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .model import Flower, FlowerImage


async def create_flower(
    *, session: AsyncSession, flower_data: Mapping[str, Any]
) -> Flower:
    flower = Flower(
        name=flower_data["name"],
        price=flower_data["price"],
        description=flower_data["description"],
        color=flower_data["color"],
    )
    session.add(flower)
    await session.flush()
    return flower


async def get_flower(*, session: AsyncSession, flower_id: int) -> Flower | None:
    statement = (
        select(Flower)
        .where(Flower.id == flower_id)
        .options(selectinload(Flower.images))
    )
    flowers = await session.execute(statement)
    return flowers.scalar_one_or_none()


async def get_flowers(*, session: AsyncSession) -> Sequence[Flower]:
    statement = select(Flower).options(selectinload(Flower.images)).order_by(Flower.id)
    flowers = await session.execute(statement)
    return flowers.scalars().all()


async def update_flower(
    *, session: AsyncSession, flower_id: int, flower_data: Mapping[str, Any]
) -> Flower | None:
    statement = (
        update(Flower)
        .where(Flower.id == flower_id)
        .values(**flower_data)
        .returning(Flower)
    )
    result = await session.execute(statement)
    await session.flush()
    return result.scalar_one_or_none()


async def delete_flower(*, session: AsyncSession, flower_id: int) -> bool:
    statement = delete(Flower).where(Flower.id == flower_id).returning(Flower.id)
    result = await session.execute(statement)
    return result.scalar_one_or_none() is not None


async def create_flower_image(
    *, session: AsyncSession, flower_id: int, url: str, sort_order: int
) -> FlowerImage:
    flower_image = FlowerImage(flower_id=flower_id, url=url, sort_order=sort_order)
    session.add(flower_image)
    await session.flush()
    return flower_image


async def get_flowers_images(*, session: AsyncSession) -> Sequence[FlowerImage]:
    statement = select(FlowerImage).order_by(FlowerImage.sort_order)
    flowers = await session.execute(statement)
    return flowers.scalars().all()


async def delete_flower_image(*, session: AsyncSession, image_id: int) -> str | None:
    statement = (
        delete(FlowerImage).where(FlowerImage.id == image_id).returning(FlowerImage.url)
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def get_flower_price(*, session: AsyncSession, flower_id: int) -> Decimal | None:
    statement = select(Flower.price).where(Flower.id == flower_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def get_flower_by_id(*, session: AsyncSession, flower_id: int) -> Flower | None:
    statement = (
        select(Flower)
        .options(selectinload(Flower.images))
        .where(Flower.id == flower_id)
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none()
