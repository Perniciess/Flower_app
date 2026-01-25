import uuid
from collections.abc import Sequence
from decimal import Decimal
from pathlib import Path

import anyio
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import FlowerNotFoundError

from . import repository as flower_repository
from .schema import FlowerCreate, FlowerImageResponse, FlowerResponse, FlowerUpdate


async def create_flower(*, session: AsyncSession, flower_data: FlowerCreate) -> FlowerResponse:
    """
    Создает новый цветок в базе данных.

    Args:
        session: сессия базы данных
        flower_data: данные для создания цветка

    Returns:
        FlowerResponse с данными созданного цветка
    """
    flower = await flower_repository.create_flower(session=session, flower_data=flower_data.model_dump())
    flower = await flower_repository.get_flower_by_id(session=session, flower_id=flower.id)
    return FlowerResponse.model_validate(flower)


async def get_flowers(*, session: AsyncSession) -> Sequence[FlowerResponse]:
    """
    Получает список цветов из базы данных.

    Args:
        session: сессия базы данных

    Returns:
        Sequence[FlowerResponse] список цветов
    """
    flowers = await flower_repository.get_flowers(session=session)
    return [FlowerResponse.model_validate(flower) for flower in flowers]


async def update_flower(*, session: AsyncSession, flower_id: int, flower_data: FlowerUpdate) -> FlowerResponse:
    """
    Обновляет данные цветка в базе данных.

    Args:
        session: сессия базы данных
        flower_id: идентификатор цветка
        flower_data: новые данные цветка

    Returns:
        FlowerResponse с данными обновленного цветка
    """
    flower = await flower_repository.update_flower(
        session=session, flower_id=flower_id, flower_data=flower_data.model_dump(exclude_unset=True)
    )
    return FlowerResponse.model_validate(flower)


async def delete_flower(*, session: AsyncSession, flower_id: int) -> bool:
    """
    Удаляет цветок из базы данных.

    Args:
        session: сессия базы данных
        flower_id: идентификатор цветка

    Returns:
        bool: цветок удален или нет
    """
    deleted = await flower_repository.delete_flower(session=session, flower_id=flower_id)
    if not deleted:
        raise FlowerNotFoundError(flower_id=flower_id)
    return True


async def upload_image(*, session: AsyncSession, flower_id: int, image: UploadFile, sort_order: int) -> FlowerImageResponse:
    """
    Загружает изображение цветка.

    Args:
        session: сессия базы данных
        flower_id: идентификатор цветка
        image: файл изображения цветка
        sort_order: порядок сортировка изображений

    Returns:
        FlowerImageResponse с данными изображения цветка

    Raises:
        ValueError: если файл без имени
    """
    if not image.filename:
        raise ValueError("Файл без имени")

    settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    ext = Path(image.filename).suffix
    filename = f"{uuid.uuid4()}{ext}"
    file_path = settings.UPLOAD_DIR / filename

    content = await image.read()
    async with await anyio.open_file(file_path, "wb") as f:
        await f.write(content)

    url = f"/static/uploads/flowers/{filename}"
    flower_image = await flower_repository.create_flower_image(session=session, flower_id=flower_id, url=url, sort_order=sort_order)
    return FlowerImageResponse.model_validate(flower_image)


async def get_flowers_images(*, session: AsyncSession) -> Sequence[FlowerImageResponse]:
    """
    Получает список изображений цветка.

    Args:
        session: сессия базы данных

    Returns:
        Sequence[FlowerImageResponse] список изображений цветка
    """
    flowers_images = await flower_repository.get_flowers_images(session=session)
    return [FlowerImageResponse.model_validate(images) for images in flowers_images]


async def delete_flower_image(*, session: AsyncSession, image_id: int) -> bool:
    """
    Удаляет изображение цветка.

    Args:
        session: сессия базы данных
        image_id: идентификатор изображения

    Returns:
        bool: изображение удалено или нет
    """
    url = await flower_repository.delete_flower_image(session=session, image_id=image_id)
    if url is None:
        raise FlowerNotFoundError(flower_id=image_id)

    file_path = settings.ROOT_DIR / url.lstrip("/")
    if file_path.exists():
        file_path.unlink()

    return True


async def get_flower_price(*, session: AsyncSession, flower_id: int) -> Decimal:
    """
    Получает цену цветка.

    Args:
        session: сессия базы данных
        flower_id: идентификатор цветка

    Returns:
        Decimal: цена цветка
    """
    price = await flower_repository.get_flower_price(session=session, flower_id=flower_id)
    if price is None:
        raise FlowerNotFoundError(flower_id=flower_id)
    return price
