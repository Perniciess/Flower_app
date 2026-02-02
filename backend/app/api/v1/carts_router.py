from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_admin, require_client
from app.db.session import get_db
from app.models.users_model import User
from app.schemas.carts_schema import CartItemResponse, CartItemUpdate, CartResponse
from app.service import carts_service

cart_router = APIRouter(prefix="/carts", tags=["carts"])


@cart_router.get(
    "", response_model=CartResponse, status_code=status.HTTP_200_OK, summary="Получить корзину текущего пользователя"
)
async def get_current_user_cart(
    user: User = Depends(require_client), session: AsyncSession = Depends(get_db)
) -> CartResponse:
    """
    Получить корзину текущего пользователя.

    Требует авторизации.
    """
    cart = await carts_service.get_current_user_cart(session=session, user_id=user.id)
    return cart


@cart_router.delete("/{cart_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить корзину")
async def delete_cart(
    cart_id: int,
    user: User = Depends(require_admin),
    session: AsyncSession = Depends(get_db),
):
    """
    Удалить корзину пользователя.

    Требует авторизации.
    """
    await carts_service.delete_cart(session=session, cart_id=cart_id)


@cart_router.post(
    "/cart_item/{product_id}",
    response_model=CartItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Добавить товар в корзину",
)
async def create_cart_item(
    product_id: int,
    quantity: int = Body(gt=0),
    current_user: User = Depends(require_client),
    target_user_id: int | None = Body(default=None),
    session: AsyncSession = Depends(get_db),
) -> CartItemResponse:
    """
    Добавить товар в корзину.

    Требует авторизации.
    """
    cart_item = await carts_service.create_cart_item(
        session=session,
        current_user=current_user,
        target_user_id=target_user_id,
        product_id=product_id,
        quantity=quantity,
    )
    return cart_item


@cart_router.patch(
    "/cart_item/{cart_item_id}",
    response_model=CartItemUpdate,
    status_code=status.HTTP_200_OK,
    summary="Обновить количество товара в корзине",
)
async def update_cart_item_quantity(
    cart_item_id: int,
    quantity: int = Body(..., ge=1, description="Новое количество товара"),
    current_user: User = Depends(require_client),
    session: AsyncSession = Depends(get_db),
) -> CartItemResponse:
    """
    Изменить количество товара в корзине.

    Требует авторизации.
    """
    cart_item = await carts_service.update_cart_item_quantity(
        session=session,
        cart_item_id=cart_item_id,
        quantity=quantity,
        current_user=current_user,
    )
    return cart_item


@cart_router.delete(
    "/cart_item/{cart_item_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить товар из корзины"
)
async def delete_cart_item(
    cart_item_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_client),
) -> None:
    """
    Удалить товар из корзины.

    Требует авторизации.
    """
    await carts_service.delete_cart_item(session=session, cart_item_id=cart_item_id, current_user=current_user)
