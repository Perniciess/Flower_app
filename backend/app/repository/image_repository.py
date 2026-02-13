from sqlalchemy.ext.asyncio import AsyncSession

from app.models.image_model import Image
from app.schemas.image_schema import ImageCreate


async def create_image(*, session: AsyncSession, image_data: ImageCreate) -> Image:
    image = Image(**image_data.model_dump())
    session.add(image)
    await session.flush()
    return image
