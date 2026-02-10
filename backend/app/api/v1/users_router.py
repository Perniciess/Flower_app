from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user, require_admin
from app.db.session import get_db
from app.models.users_model import User
from app.schemas.users_schema import UserResponse, UserUpdate
from app.service import users_service

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get(
    "/",
    response_model=Page[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Получить список всех пользователей",
)
async def get_users(
    session: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)
) -> Page[UserResponse]:
    """
    Получить список всех пользователей.

    Требует прав администратора.
    """
    users = await users_service.get_users(session=session)
    return users


@user_router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить активного пользователя",
)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Получить данные активного пользователя.

    Требует авторизации.
    """
    return current_user


@user_router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить пользователя по ID",
)
async def get_user_by_id(
    user_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> UserResponse:
    """
    Получить пользователя по идентификатору.

    Требует прав администратора.
    """
    return await users_service.get_user_by_id(session=session, user_id=user_id)


@user_router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Обновить данные пользователя",
)
async def update_user(
    user_id: int,
    data: UserUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> UserResponse:
    """
    Обновить данные пользователя.

    Требует прав администратора.
    """
    return await users_service.update_user(session=session, user_id=user_id, data=data)
