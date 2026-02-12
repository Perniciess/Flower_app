from sqlalchemy.ext.asyncio import AsyncSession

from app.models.banners_model import Banner
from app.schemas.banners_schema import BannerCreate


async def create_advice(*, session: AsyncSession, banner_data: BannerCreate) -> Banner:
    banner = Banner(**banner_data.model_dump())
    session.add(banner)
    await session.flush()
    return banner
