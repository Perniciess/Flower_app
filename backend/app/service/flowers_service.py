from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import FlowerNotFoundError, ProductNotFoundError
from app.repository import flowers_repository
from app.schemas.flowers_schema import (
    CompositionItem,
    FlowerCreate,
    FlowerResponse,
    FlowerUpdate,
)


async def create_flower(*, session: AsyncSession, flower_data: FlowerCreate) -> FlowerResponse:
    flower = await flowers_repository.create_flower(session=session, flower_data=flower_data)
    return FlowerResponse.model_validate(flower)


async def get_flower(*, session: AsyncSession, flower_id: int) -> FlowerResponse:
    flower = await flowers_repository.get_flower(session=session, flower_id=flower_id)
    if flower is None:
        raise FlowerNotFoundError(flower_id=flower_id)
    return FlowerResponse.model_validate(flower)


async def get_flowers(*, session: AsyncSession) -> Sequence[FlowerResponse]:
    flowers = await flowers_repository.get_flowers(session=session)
    return [FlowerResponse.model_validate(f) for f in flowers]


async def update_flower(*, session: AsyncSession, flower_id: int, flower_data: FlowerUpdate) -> FlowerResponse:
    flower = await flowers_repository.update_flower(session=session, flower_id=flower_id, flower_data=flower_data)
    if flower is None:
        raise FlowerNotFoundError(flower_id=flower_id)
    return FlowerResponse.model_validate(flower)


async def delete_flower(*, session: AsyncSession, flower_id: int) -> bool:
    deleted = await flowers_repository.delete_flower(session=session, flower_id=flower_id)
    if not deleted:
        raise FlowerNotFoundError(flower_id=flower_id)
    return True


async def set_product_composition(*, session: AsyncSession, product_id: int, items: list[CompositionItem]) -> None:
    product = await flowers_repository.get_product_for_composition(session=session, product_id=product_id)
    if product is None:
        raise ProductNotFoundError(product_id=product_id)

    for item in items:
        flower = await flowers_repository.get_flower(session=session, flower_id=item.flower_id)
        if flower is None:
            raise FlowerNotFoundError(flower_id=item.flower_id)

    await flowers_repository.set_product_composition(session=session, product_id=product_id, items=items)
