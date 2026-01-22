from collections.abc import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user, require_admin
from app.database.session import get_db

from . import service as user_service
from .model import User
from .schema import UserResponse, UserUpdate

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("/", response_model=Sequence[UserResponse])
async def get_users(session: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)) -> Sequence[UserResponse]:
    users = await user_service.get_users(session=session)
    return users


@user_router.get("/me", response_model=UserResponse)
async def get_me(current_user=Depends(get_current_user)):
    return current_user


@user_router.get("/{user_id:int}", response_model=UserResponse)
async def get_user_by_id(
    user_id: int, session: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)
) -> UserResponse:
    return await user_service.get_user_by_id(session=session, user_id=user_id)


@user_router.patch("/{user_id:int}", response_model=UserResponse)
async def update_user(
    user_id: int, data: UserUpdate, session: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)
) -> UserResponse:
    return await user_service.update_user(session=session, user_id=user_id, data=data)
