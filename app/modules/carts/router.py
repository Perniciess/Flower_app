from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.database.session import get_db
from app.modules.users.model import User

from . import service as cart_service

cart_router = APIRouter(prefix="/carts", tags=["carts"])


@cart_router.post("/create")
async def create_cart(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    cart = await cart_service.create_cart(session=session, user_id=user.id)
    return cart


@cart_router.delete("/{cart_id}", status_code=204)
async def delete_cart(cart_id: int, session: AsyncSession = Depends(get_db)):
    await cart_service.delete_cart(session=session, cart_id=cart_id)
