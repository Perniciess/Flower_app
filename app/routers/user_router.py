from collections.abc import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_active_user
from app.database.session import get_db
from app.schemas.user_schemas import UserOutput, UserUpdate
from app.services import user_service

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("/", response_model=Sequence[UserOutput])
async def get_users(session: AsyncSession = Depends(get_db)) -> Sequence[UserOutput]:
    users = await user_service.get_users(session=session)
    return users


@user_router.get("/me", response_model=UserOutput)
async def get_me(current_user=Depends(get_current_active_user)):
    return current_user


@user_router.get("/{user_id:int}", response_model=UserOutput)
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_db)) -> UserOutput:
    return await user_service.get_user_by_id(session=session, user_id=user_id)


@user_router.patch("/{user_id:int}", response_model=UserOutput)
async def update_user(user_id: int, data: UserUpdate, session: AsyncSession = Depends(get_db)) -> UserOutput:
    return await user_service.update_user(session=session, user_id=user_id, data=data)
