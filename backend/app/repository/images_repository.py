from collections.abc import Sequence

from sqlalchemy import Select, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.advices_model import Advice
from app.models.banners_model import Banner
from app.models.categories_model import Category
from app.models.images_model import Image
from app.models.products_model import ProductImage
from app.schemas.image_schema import ImageCreate, ImageUpdate


async def create_image(*, session: AsyncSession, image_data: ImageCreate) -> Image:
    image = Image(**image_data.model_dump())
    session.add(image)
    await session.flush()
    return image


async def get_image(*, session: AsyncSession, image_id: int) -> Image | None:
    statement = select(Image).where(Image.id == image_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def get_images(*, session: AsyncSession) -> Sequence[Image]:
    statement = select(Image).order_by(Image.id)
    result = await session.execute(statement)
    return result.scalars().all()


def get_images_query() -> Select[tuple[Image]]:
    statement = select(Image).order_by(Image.id)
    return statement


async def get_image_by_hash(*, session: AsyncSession, hash: str) -> Image | None:
    statement = select(Image).where(Image.hash == hash)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def update_image(
    *, session: AsyncSession, image_id: int, image_data: ImageUpdate
) -> Image | None:
    statement = (
        update(Image)
        .where(Image.id == image_id)
        .values(**image_data.model_dump(exclude_unset=True))
        .returning(Image)
    )
    result = await session.execute(statement)
    await session.flush()
    return result.scalar_one_or_none()


async def delete_image(*, session: AsyncSession, image_id: int) -> bool:
    statement = delete(Image).where(Image.id == image_id).returning(Image.id)
    result = await session.execute(statement)
    return result.scalar_one_or_none() is not None


async def is_image_referenced(*, session: AsyncSession, image_id: int) -> bool:
    """Проверяет, используется ли изображение где-либо."""

    checks = [
        select(Banner.id).where(Banner.image_id == image_id).limit(1),
        select(Category.id).where(Category.image_id == image_id).limit(1),
        select(Advice.id).where(Advice.image_id == image_id).limit(1),
        select(ProductImage.id).where(ProductImage.image_id == image_id).limit(1),
    ]

    for stmt in checks:
        result = await session.execute(stmt)
        if result.scalar_one_or_none():
            return True
    return False
