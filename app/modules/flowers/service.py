import uuid
from collections.abc import Sequence
from decimal import Decimal
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import FlowerNotFoundError

from . import repository as flower_repository
from .schema import FlowerCreate, FlowerImageResponse, FlowerResponse, FlowerUpdate

UPLOAD_DIR = Path("app/static/uploads/flowers")


async def create_flower(*, session: AsyncSession, flower_data: FlowerCreate) -> FlowerResponse:
    flower = await flower_repository.create_flower(session=session, flower_data=flower_data.model_dump())
    flower = await flower_repository.get_flower_by_id(session=session, flower_id=flower.id)
    return FlowerResponse.model_validate(flower)


async def get_flowers(*, session: AsyncSession) -> Sequence[FlowerResponse]:
    flowers = await flower_repository.get_flowers(session=session)
    return [FlowerResponse.model_validate(flower) for flower in flowers]


async def update_flower(*, session: AsyncSession, flower_id: int, flower_data: FlowerUpdate) -> FlowerResponse:
    flower = await flower_repository.update_flower(
        session=session, flower_id=flower_id, flower_data=flower_data.model_dump(exclude_unset=True)
    )
    return FlowerResponse.model_validate(flower)


async def delete_flower(*, session: AsyncSession, flower_id: int) -> bool:
    deleted = await flower_repository.delete_flower(session=session, flower_id=flower_id)
    if not deleted:
        raise FlowerNotFoundError(flower_id=flower_id)
    return True


async def upload_image(*, session: AsyncSession, flower_id: int, image: UploadFile, sort_order: int) -> FlowerImageResponse:
    if not image.filename:
        raise ValueError("Файл без имени")

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    ext = Path(image.filename).suffix
    filename = f"{uuid.uuid4()}{ext}"
    file_path = UPLOAD_DIR / filename

    content = await image.read()
    with open(file_path, "wb") as f:
        f.write(content)

    url = f"/static/uploads/flowers/{filename}"
    flower_image = await flower_repository.create_flower_image(session=session, flower_id=flower_id, url=url, sort_order=sort_order)
    return FlowerImageResponse.model_validate(flower_image)


async def get_flowers_images(*, session: AsyncSession) -> Sequence[FlowerImageResponse]:
    flowers_images = await flower_repository.get_flowers_images(session=session)
    return [FlowerImageResponse.model_validate(images) for images in flowers_images]


async def delete_flower_image(*, session: AsyncSession, image_id: int) -> bool:
    url = await flower_repository.delete_flower_image(session=session, image_id=image_id)
    if url is None:
        raise FlowerNotFoundError(flower_id=image_id)

    file_path = Path("app") / url.lstrip("/")
    if file_path.exists():
        file_path.unlink()

    return True


async def get_flower_price(*, session: AsyncSession, flower_id: int) -> Decimal:
    price = await flower_repository.get_flower_price(session=session, flower_id=flower_id)
    if price is None:
        raise FlowerNotFoundError(flower_id=flower_id)
    return price
