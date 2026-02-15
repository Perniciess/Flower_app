from collections.abc import Sequence
from decimal import Decimal

from sqlalchemy import Select, delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.products_model import Product, ProductImage
from app.schemas.products_schema import ProductCreate, ProductUpdate


async def create_product(
    *, session: AsyncSession, product_data: ProductCreate
) -> Product:
    statement = Product(**product_data.model_dump())
    session.add(statement)
    await session.flush()
    return statement


async def get_product(*, session: AsyncSession, product_id: int) -> Product | None:
    statement = (
        select(Product)
        .where(Product.id == product_id)
        .options(
            selectinload(Product.images),
            selectinload(Product.categories),
            selectinload(Product.composition),
        )
    )
    product = await session.execute(statement)
    return product.scalar_one_or_none()


def get_products_query() -> Select[tuple[Product]]:
    return (
        select(Product)
        .options(
            selectinload(Product.images),
            selectinload(Product.categories),
            selectinload(Product.composition),
        )
        .order_by(Product.sort_order)
    )


async def update_product(
    *, session: AsyncSession, product_id: int, product_data: ProductUpdate
) -> Product | None:
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


async def create_product_image(
    *, session: AsyncSession, product_id: int, image_id: int, sort_order: int
) -> ProductImage:
    product_image = ProductImage(
        product_id=product_id, image_id=image_id, sort_order=sort_order
    )
    session.add(product_image)
    await session.flush()
    await session.refresh(product_image, ["image"])
    return product_image


async def get_product_images(*, session: AsyncSession) -> Sequence[ProductImage]:
    statement = select(ProductImage).order_by(ProductImage.sort_order)
    result = await session.execute(statement)
    return result.scalars().all()


async def delete_product_image(*, session: AsyncSession, image_id: int) -> bool:
    statement = (
        delete(ProductImage)
        .where(ProductImage.id == image_id)
        .returning(ProductImage.id)
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none() is not None


async def get_product_price(
    *, session: AsyncSession, product_id: int
) -> Decimal | None:
    statement = select(Product.price).where(Product.id == product_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def get_products_by_ids(
    *, session: AsyncSession, product_ids: list[int]
) -> Sequence[Product]:
    statement = (
        select(Product)
        .where(Product.id.in_(product_ids))
        .options(
            selectinload(Product.images),
            selectinload(Product.categories),
            selectinload(Product.composition),
        )
    )
    result = await session.execute(statement)
    return result.scalars().all()


async def get_product_by_id(
    *, session: AsyncSession, product_id: int
) -> Product | None:
    statement = (
        select(Product)
        .options(selectinload(Product.images), selectinload(Product.composition))
        .where(Product.id == product_id)
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def set_all_products_in_stock(*, session: AsyncSession, in_stock: bool) -> int:
    count_stmt = (
        select(func.count()).select_from(Product).where(Product.in_stock != in_stock)
    )
    count_result = await session.execute(count_stmt)
    count = count_result.scalar() or 0

    statement = update(Product).values(in_stock=in_stock)
    await session.execute(statement)
    await session.flush()
    return count
