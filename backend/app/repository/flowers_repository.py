from collections.abc import Sequence

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.products_model import Flower, Product, bouquet_composition
from app.schemas.flowers_schema import CompositionItem, FlowerCreate, FlowerUpdate


async def create_flower(*, session: AsyncSession, flower_data: FlowerCreate) -> Flower:
    flower = Flower(**flower_data.model_dump())
    session.add(flower)
    await session.flush()
    return flower


async def get_flower(*, session: AsyncSession, flower_id: int) -> Flower | None:
    statement = select(Flower).where(Flower.id == flower_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def get_flowers(*, session: AsyncSession) -> Sequence[Flower]:
    statement = select(Flower).order_by(Flower.name)
    result = await session.execute(statement)
    return result.scalars().all()


async def update_flower(
    *, session: AsyncSession, flower_id: int, flower_data: FlowerUpdate
) -> Flower | None:
    statement = (
        update(Flower)
        .where(Flower.id == flower_id)
        .values(**flower_data.model_dump(exclude_unset=True))
        .returning(Flower)
    )
    result = await session.execute(statement)
    await session.flush()
    return result.scalar_one_or_none()


async def delete_flower(*, session: AsyncSession, flower_id: int) -> bool:
    statement = delete(Flower).where(Flower.id == flower_id).returning(Flower.id)
    result = await session.execute(statement)
    return result.scalar_one_or_none() is not None


async def set_product_composition(
    *, session: AsyncSession, product_id: int, items: list[CompositionItem]
) -> None:
    await session.execute(
        delete(bouquet_composition).where(
            bouquet_composition.c.product_id == product_id
        )
    )

    if items:
        values = [
            {
                "product_id": product_id,
                "flower_id": item.flower_id,
                "quantity": item.quantity,
            }
            for item in items
        ]
        await session.execute(insert(bouquet_composition).values(values))
    await session.flush()


async def get_product_for_composition(
    *, session: AsyncSession, product_id: int
) -> Product | None:
    statement = select(Product).where(Product.id == product_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()
