from collections.abc import Sequence
from decimal import Decimal

from fastapi import UploadFile
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import ImageNotFoundError, ProductNotFoundError
from app.repository import products_repository
from app.schemas.products_schema import (
    ProductCreate,
    ProductImageResponse,
    ProductResponse,
    ProductUpdate,
)
from app.service import discounts_service
from app.utils.filters.products import ProductFilter

from . import images_service


async def create_product(
    *,
    session: AsyncSession,
    product_data: ProductCreate,
    image: UploadFile | None = None,
) -> ProductResponse:
    """
    Создает новый товар в базе данных.

    Args:
        session: сессия базы данных
        product_data: данные для создания цветка
        image: опциональное изображение товара

    Returns:
        ProductResponse с данными созданного цветка
    """
    product = await products_repository.create_product(
        session=session, product_data=product_data
    )

    if image is not None:
        img = await images_service.create_image(
            session=session, image=image, type=settings.PRODUCTS
        )
        await products_repository.create_product_image(
            session=session, product_id=product.id, image_id=img.id, sort_order=0
        )

    product = await products_repository.get_product_by_id(
        session=session, product_id=product.id
    )
    return ProductResponse.model_validate(product)


async def get_products(
    *, session: AsyncSession, product_filter: ProductFilter
) -> Page[ProductResponse]:
    """
    Возвращает отфильтрованный пагинированный список товаров из базы данных.

    Args:
        session: сессия базы данных
        product_filter: фильтр товара

    Returns:
        Page[ProductResponse] список товаров
    """
    query = products_repository.get_products_query()
    filtered_query = product_filter.filter(query)
    sorted_query = product_filter.sort(filtered_query)
    page = await paginate(session, sorted_query)

    discount_map = await discounts_service.enrich_products(
        session=session, products=page.items
    )

    enriched_items = []
    for product in page.items:
        response = ProductResponse.model_validate(product)
        discounted_price, discount = discount_map.get(product.id, (None, None))
        response.discounted_price = discounted_price
        response.discount_percentage = discount.percentage if discount else None
        enriched_items.append(response)

    page.items = enriched_items
    return page


async def get_product(*, session: AsyncSession, product_id: int) -> ProductResponse:
    """
    Возвращает товар из базы данных.

    Args:
        session: сессия базы данных
        product_id: идентификатор товара

    Returns:
        ProductResponse информация о товаре

    Raises:
        ProductNotFoundError: если товар не найден
    """
    product = await products_repository.get_product(
        session=session, product_id=product_id
    )
    if product is None:
        raise ProductNotFoundError(product_id=product_id)

    discount_map = await discounts_service.enrich_products(
        session=session, products=[product]
    )
    response = ProductResponse.model_validate(product)
    discounted_price, discount = discount_map.get(product.id, (None, None))
    response.discounted_price = discounted_price
    response.discount_percentage = discount.percentage if discount else None
    return response


async def update_product(
    *, session: AsyncSession, product_id: int, product_data: ProductUpdate
) -> ProductResponse:
    """
    Обновляет данные товара в базе данных.

    Args:
        session: сессия базы данных
        product_id: идентификатор товара
        product_data: новые данные товара

    Returns:
        ProductResponse с данными обновленного товара
    """
    product = await products_repository.update_product(
        session=session,
        product_id=product_id,
        product_data=product_data,
    )
    return ProductResponse.model_validate(product)


async def delete_product(*, session: AsyncSession, product_id: int) -> bool:
    """
    Удаляет товар из базы данных.

    Args:
        session: сессия базы данных
        product_id: идентификатор товара

    Returns:
        bool: товар удален или нет
    """
    deleted = await products_repository.delete_product(
        session=session, product_id=product_id
    )
    if not deleted:
        raise ProductNotFoundError(product_id=product_id)
    return True


async def upload_image(
    *, session: AsyncSession, product_id: int, image: UploadFile, sort_order: int
) -> ProductImageResponse:
    """
    Загружает изображение товара.

    Args:
        session: сессия базы данных
        product_id: идентификатор товара
        image: файл изображения товара
        sort_order: порядок сортировка изображений

    Returns:
        ProductImageResponse с данными изображения товара

    Raises:
        ValueError: если файл невалидный
    """
    img = await images_service.create_image(
        session=session, image=image, type=settings.PRODUCTS
    )
    product_image = await products_repository.create_product_image(
        session=session, product_id=product_id, image_id=img.id, sort_order=sort_order
    )
    return ProductImageResponse.model_validate(product_image)


async def get_product_images(
    *,
    session: AsyncSession,
) -> Sequence[ProductImageResponse]:
    """
    Получает список изображений товара.

    Args:
        session: сессия базы данных

    Returns:
        Sequence[ProductImageResponse] список изображений товара
    """
    product_images = await products_repository.get_product_images(session=session)
    return [ProductImageResponse.model_validate(images) for images in product_images]


async def delete_product_image(*, session: AsyncSession, image_id: int) -> bool:
    """
    Удаляет изображение товара.

    Args:
        session: сессия базы данных
        image_id: идентификатор изображения

    Returns:
        bool: изображение удалено или нет
    """
    deleted = await products_repository.delete_product_image(
        session=session, image_id=image_id
    )
    if not deleted:
        raise ImageNotFoundError(image_id=image_id)
    return True


async def get_product_price(*, session: AsyncSession, product_id: int) -> Decimal:
    price = await products_repository.get_product_price(
        session=session, product_id=product_id
    )
    if price is None:
        raise ProductNotFoundError(product_id=product_id)
    return price


async def set_all_products_in_stock(*, session: AsyncSession, in_stock: bool) -> int:
    return await products_repository.set_all_products_in_stock(
        session=session, in_stock=in_stock
    )


async def attach_image(
    *, session: AsyncSession, product_id: int, image_id: int, sort_order: int = 0
) -> ProductImageResponse:
    product = await products_repository.get_product(
        session=session, product_id=product_id
    )
    if product is None:
        raise ProductNotFoundError(product_id=product_id)

    await images_service.get_image(session=session, image_id=image_id)

    product_image = await products_repository.create_product_image(
        session=session, product_id=product_id, image_id=image_id, sort_order=sort_order
    )
    return ProductImageResponse.model_validate(product_image)
