from collections.abc import Sequence

from fastapi import APIRouter, Depends, Form, UploadFile
from fastapi_filter import FilterDepends
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_admin
from app.database.session import get_db
from app.modules.users.model import User

from . import service as product_service
from .filter import ProductFilter
from .schema import ProductCreate, ProductImageResponse, ProductResponse, ProductUpdate

product_router = APIRouter(prefix="/products", tags=["products"])


@product_router.post("/create", response_model=ProductResponse, summary="Создать товар")
async def create_product(
    product_data: ProductCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> ProductResponse:
    """
    Создание товара

    Требует прав администратора
    """
    product = await product_service.create_product(session=session, product_data=product_data)
    return product


@product_router.get("/", response_model=Page[ProductResponse], summary="Получить список товаров")
async def get_products(
    session: AsyncSession = Depends(get_db),
    product_filter: ProductFilter = FilterDepends(ProductFilter),
) -> Page[ProductResponse]:
    """Получение списка товаров"""
    products = await product_service.get_products(session=session, product_filter=product_filter)
    return products


@product_router.get("/{product_id}", response_model=ProductResponse, summary="Получить один товар")
async def get_product_by_id(product_id: int, session: AsyncSession = Depends(get_db)):
    product = await product_service.get_product(session=session, product_id=product_id)
    return product


@product_router.patch("/{product_id:int}", response_model=ProductResponse, summary="Получить товар по ID")
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> ProductResponse:
    """
    Изменение информации о товаре.

    Требует прав администратора.
    """
    product = await product_service.update_product(session=session, product_id=product_id, product_data=product_data)
    return product


@product_router.delete("/{product_id:int}", status_code=204, summary="Удалить товар")
async def delete_product(
    product_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Удаление товара.

    Требует прав администратора.
    """
    await product_service.delete_product(session=session, product_id=product_id)


@product_router.post(
    "/images/{product_id:int}",
    response_model=ProductImageResponse,
    summary="Загрузить изображение товара",
)
async def upload_image(
    product_id: int,
    image: UploadFile,
    sort_order: int = Form(default=0),
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> ProductImageResponse:
    """
    Добавление изображения товара.

    Требует прав администратора.
    """
    product_image = await product_service.upload_image(
        session=session, product_id=product_id, image=image, sort_order=sort_order
    )
    return product_image


@product_router.get(
    "/images",
    response_model=Sequence[ProductImageResponse],
    summary="Получить изображения товара",
)
async def get_products_images(
    session: AsyncSession = Depends(get_db),
) -> Sequence[ProductImageResponse]:
    """Получение изображений товара."""
    images = await product_service.get_product_images(session=session)
    return images


@product_router.delete("/images/{image_id:int}", status_code=204, summary="Удалить изображение товара")
async def delete_product_image(
    image_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Удаление изображения товара.

    Требует прав администратора.
    """
    await product_service.delete_product_image(session=session, image_id=image_id)
