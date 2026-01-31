from collections.abc import Sequence
from decimal import Decimal

from sqlalchemy import Select, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .model import Product, ProductImage
from .schema import ProductCreate, ProductUpdate


async def create_product(*, session: AsyncSession, product_data: ProductCreate) -> Product:
    statement = Product(**product_data.model_dump())
    session.add(statement)
    await session.flush()
    return statement


async def get_product(*, session: AsyncSession, product_id: int) -> Product | None:
    statement = (
        select(Product)
        .where(Product.id == product_id)
        .options(selectinload(Product.images), selectinload(Product.categories))
    )
    product = await session.execute(statement)
    return product.scalar_one_or_none()


def get_products_query() -> Select[tuple[Product]]:
    return select(Product).options(selectinload(Product.images), selectinload(Product.categories))


async def update_product(*, session: AsyncSession, product_id: int, product_data: ProductUpdate) -> Product | None:
    statement = (
        update(Product)
        .where(Product.id == product_id)
        .values(**product_data.model_dump(exclude_unset=True))
        .returning(Product)
    )
    result = await session.execute(statement)
    await session.flush()
    return result.scalar_one_or_none()


async def delete_product(*, session: AsyncSession, product_id: int) -> bool:
    statement = delete(Product).where(Product.id == product_id).returning(Product.id)
    result = await session.execute(statement)
    return result.scalar_one_or_none() is not None


async def create_product_image(*, session: AsyncSession, product_id: int, url: str, sort_order: int) -> ProductImage:
    statement = ProductImage(product_id=product_id, url=url, sort_order=sort_order)
    session.add(statement)
    await session.flush()
    return statement


async def get_product_images(*, session: AsyncSession) -> Sequence[ProductImage]:
    statement = select(ProductImage).order_by(ProductImage.sort_order)
    result = await session.execute(statement)
    return result.scalars().all()


async def delete_product_image(*, session: AsyncSession, image_id: int) -> str | None:
    statement = delete(ProductImage).where(ProductImage.id == image_id).returning(ProductImage.url)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def get_product_price(*, session: AsyncSession, product_id: int) -> Decimal | None:
    statement = select(Product.price).where(Product.id == product_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def get_product_by_id(*, session: AsyncSession, product_id: int) -> Product | None:
    statement = select(Product).options(selectinload(Product.images)).where(Product.id == product_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()
