from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_client
from app.database.session import get_db
from app.modules.users.model import User

from . import service as order_service

order_router = APIRouter(prefix="/orders", tags=["orders"])


@order_router.post("/create", summary="Создание заказа")
async def create_order(user: User = Depends(require_client), session: AsyncSession = Depends(get_db)):
    await order_service.create_order(session=session, user_id=user.id)
