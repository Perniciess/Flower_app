from collections.abc import Sequence
from decimal import Decimal

from fastapi import APIRouter, Depends, Form, Request, UploadFile, status
from fastapi_filter import FilterDepends
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_admin
from app.core.limiter import limiter
from app.db.session import get_db
from app.models.users_model import User
from app.schemas.flowers_schema import SetCompositionRequest
from app.schemas.products_schema import (
    ProductCreate,
    ProductImageResponse,
    ProductResponse,
    ProductUpdate,
)
from app.service import flowers_service, products_service
from app.utils.filters.products import ProductFilter

product_router = APIRouter(prefix="/products", tags=["products"])


@product_router.post(
    "/create",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать товар",
)
async def create_product(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
    name: str = Form(..., max_length=255, description="Название товара"),
    price: Decimal = Form(..., gt=0, description="Стоимость товара"),
    description: str = Form(..., max_length=2000, description="Описание"),
    color: str = Form(..., max_length=64, description="Цвет"),
    is_active: bool = Form(default=True, description="Активен ли товар"),
    in_stock: bool = Form(default=True, description="В наличии"),
    image: UploadFile | None = None,
) -> ProductResponse:
    """
    Создать товар.

    Требует прав администратора.
    """
    product_data = ProductCreate(
        name=name,
        price=price,
        description=description,
        color=color,
        is_active=is_active,
        in_stock=in_stock,
    )
    product = await products_service.create_product(session=session, product_data=product_data, image=image)
    return product


@product_router.get(
    "/",
    response_model=Page[ProductResponse],
    status_code=status.HTTP_200_OK,
    summary="Получить список товаров",
)
@limiter.limit("30/minute")
async def get_products(
    request: Request,
    session: AsyncSession = Depends(get_db),
    product_filter: ProductFilter = FilterDepends(ProductFilter),
) -> Page[ProductResponse]:
    """Получить список товаров."""
    products = await products_service.get_products(session=session, product_filter=product_filter)
    return products


@product_router.get(
    "/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить один товар",
)
@limiter.limit("60/minute")
async def get_product_by_id(request: Request, product_id: int, session: AsyncSession = Depends(get_db)):
    """Получить товар по ID."""
    product = await products_service.get_product(session=session, product_id=product_id)
    return product


@product_router.patch(
    "/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить товар по ID",
)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> ProductResponse:
    """
    Измененить информацию о товаре.

    Требует прав администратора.
    """
    product = await products_service.update_product(session=session, product_id=product_id, product_data=product_data)
    return product


@product_router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить товар")
async def delete_product(
    product_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Удалить товара.

    Требует прав администратора.
    """
    await products_service.delete_product(session=session, product_id=product_id)


@product_router.post(
    "/images/{product_id}",
    response_model=ProductImageResponse,
    status_code=status.HTTP_201_CREATED,
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
    Загрузить изображения товара.

    Требует прав администратора.
    """
    product_image = await products_service.upload_image(
        session=session, product_id=product_id, image=image, sort_order=sort_order
    )
    return product_image


@product_router.get(
    "/images",
    response_model=Sequence[ProductImageResponse],
    status_code=status.HTTP_200_OK,
    summary="Получить изображения товара",
)
async def get_products_images(
    session: AsyncSession = Depends(get_db),
) -> Sequence[ProductImageResponse]:
    """Получить изображений товара."""
    images = await products_service.get_product_images(session=session)
    return images


@product_router.delete(
    "/images/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить изображение товара",
)
async def delete_product_image(
    image_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    await products_service.delete_product_image(session=session, image_id=image_id)


@product_router.put(
    "/{product_id}/composition",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Установить состав букета",
)
async def set_product_composition(
    product_id: int,
    request: SetCompositionRequest,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> None:
    await flowers_service.set_product_composition(session=session, product_id=product_id, items=request.items)


@product_router.post("/bulk/close", status_code=status.HTTP_200_OK, summary="Закрыть все товары к заказу")
async def close_all_products(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> dict[str, int]:
    count = await products_service.set_all_products_in_stock(session=session, in_stock=False)
    return {"updated": count}


@product_router.post("/bulk/open", status_code=status.HTTP_200_OK, summary="Открыть все товары к заказу")
async def open_all_products(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> dict[str, int]:
    count = await products_service.set_all_products_in_stock(session=session, in_stock=True)
    return {"updated": count}
