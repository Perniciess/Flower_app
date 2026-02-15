from collections.abc import Sequence

from sqlalchemy import Select, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.banners_model import Banner
from app.schemas.banners_schema import BannerCreate, BannerUpdate


async def create_banner(
    *, session: AsyncSession, banner_data: BannerCreate, image_id: int | None
) -> Banner:
    banner = Banner(**banner_data.model_dump(), image_id=image_id)
    session.add(banner)
    await session.flush()
    return banner


async def get_banner(*, session: AsyncSession, banner_id: int) -> Banner | None:
    statement = select(Banner).where(Banner.id == banner_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def get_banners(
    *, session: AsyncSession, only_active: bool = False
) -> Sequence[Banner]:
    statement = select(Banner).order_by(Banner.sort_order, Banner.id)
    if only_active:
        statement = statement.where(Banner.is_active)
    result = await session.execute(statement)
    return result.scalars().all()


def get_banners_query(*, only_active: bool = False) -> Select[tuple[Banner]]:
    statement = select(Banner).order_by(Banner.sort_order, Banner.id)
    if only_active:
        statement = statement.where(Banner.is_active)
    return statement


async def update_banner(
    *,
    session: AsyncSession,
    banner_id: int,
    banner_data: BannerUpdate,
    image_id: int | None = None,
) -> Banner | None:
    update_data = banner_data.model_dump(exclude_unset=True)
    if image_id is not None:
        update_data["image_id"] = image_id
    statement = (
        update(Banner)
        .where(Banner.id == banner_id)
        .values(**update_data)
        .returning(Banner)
    )
    result = await session.execute(statement)
    await session.flush()
    return result.scalar_one_or_none()


async def delete_banner(*, session: AsyncSession, banner_id: int) -> bool:
    statement = delete(Banner).where(Banner.id == banner_id).returning(Banner.id)
    result = await session.execute(statement)
    return result.scalar_one_or_none() is not None


async def set_banner_image(
    *, session: AsyncSession, banner_id: int, image_id: int | None
) -> Banner | None:
    statement = (
        update(Banner)
        .where(Banner.id == banner_id)
        .values(image_id=image_id)
        .returning(Banner)
    )
    result = await session.execute(statement)
    await session.flush()
    return result.scalar_one_or_none()
