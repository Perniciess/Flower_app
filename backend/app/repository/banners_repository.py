from collections.abc import Sequence

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.banners_model import Banner
from app.schemas.banners_schema import BannerCreate, BannerUpdate


async def create_banner(*, session: AsyncSession, banner_data: BannerCreate) -> Banner:
    banner = Banner(**banner_data.model_dump())
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


async def update_banner(
    *, session: AsyncSession, banner_id: int, banner_data: BannerUpdate
) -> Banner | None:
    statement = (
        update(Banner)
        .where(Banner.id == banner_id)
        .values(**banner_data.model_dump(exclude_unset=True))
        .returning(Banner)
    )
    result = await session.execute(statement)
    await session.flush()
    return result.scalar_one_or_none()


async def update_banner_image(
    *, session: AsyncSession, banner_id: int, image_url: str
) -> Banner | None:
    statement = (
        update(Banner)
        .where(Banner.id == banner_id)
        .values(image_url=image_url)
        .returning(Banner)
    )
    result = await session.execute(statement)
    await session.flush()
    return result.scalar_one_or_none()


async def delete_banner(*, session: AsyncSession, banner_id: int) -> str | None:
    statement = delete(Banner).where(Banner.id == banner_id).returning(Banner.image_url)
    result = await session.execute(statement)
    return result.scalar_one_or_none()
