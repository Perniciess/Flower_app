from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_admin, require_client
from app.database.session import get_db
from app.modules.users.model import User

from . import service as cart_service
from .schema import CartItemUpdate, CartResponse

cart_router = APIRouter(prefix="/carts", tags=["carts"])


@cart_router.post("/create", response_model=CartResponse)
async def create_cart(user: User = Depends(require_client), session: AsyncSession = Depends(get_db)) -> CartResponse:
    cart = await cart_service.create_cart(session=session, user_id=user.id)
    return cart


@cart_router.delete("/{cart_id}", status_code=204)
async def delete_cart(cart_id: int, user: User = Depends(require_admin), session: AsyncSession = Depends(get_db)):
    await cart_service.delete_cart(session=session, cart_id=cart_id, user_id=user.id)


@cart_router.post("/cart_item/{flower_id}")
async def create_cart_item(
    flower_id: int,
    quantity: int,
    current_user: User = Depends(require_client),
    target_user_id: int | None = None,
    session: AsyncSession = Depends(get_db),
):
    cart_item = await cart_service.create_cart_item(
        session=session, current_user=current_user, target_user_id=target_user_id, flower_id=flower_id, quantity=quantity
    )
    return cart_item


@cart_router.patch("/cart_item/{cart_item_id}")
async def update_cart_item_quantity(
    cart_item_id: int, quantity: int, current_user: User = Depends(require_client), session: AsyncSession = Depends(get_db)
) -> CartItemUpdate:
    cart_item = await cart_service.update_cart_item_quantity(
        session=session, cart_item_id=cart_item_id, quantity=quantity, current_user=current_user
    )
    return cart_item
