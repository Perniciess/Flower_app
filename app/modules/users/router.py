from collections.abc import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user, require_admin
from app.database.session import get_db

from . import service as user_service
from .model import User
from .schema import UserResponse, UserUpdate

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("/", response_model=Sequence[UserResponse], summary="Получить список всех пользователей")
async def get_users(session: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)) -> Sequence[UserResponse]:
    """
    Получить список всех пользователей\n
    Требует прав администратора
    """
    users = await user_service.get_users(session=session)
    return users


@user_router.get("/me", response_model=UserResponse, summary="Получить активного пользователя")
async def get_me(current_user=Depends(get_current_user)):
    """Получить данные активного пользователя"""
    return current_user


@user_router.get("/{user_id:int}", response_model=UserResponse, summary="Получить пользователя по ID")
async def get_user_by_id(
    user_id: int, session: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)
) -> UserResponse:
    """
    Получить пользователя по идентификатору\n
    Требует прав администратора
    """
    return await user_service.get_user_by_id(session=session, user_id=user_id)


@user_router.patch("/{user_id:int}", response_model=UserResponse, summary="Обновить данные пользователя")
async def update_user(
    user_id: int, data: UserUpdate, session: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)
) -> UserResponse:
    """
    Обновить данные пользователя\n
    Требует прав администратора
    """
    return await user_service.update_user(session=session, user_id=user_id, data=data)
