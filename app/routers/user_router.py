from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UserNotFoundError
from app.database.session import get_db
from app.schemas.user_schemas import UserOutput
from app.services import user_service

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("/", response_model=Sequence[UserOutput])
async def get_users(session: AsyncSession = Depends(get_db)) -> Sequence[UserOutput]:
    users = await user_service.get_users(session=session)
    return users


@user_router.get("/{user_id}", response_model=UserOutput)
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_db)) -> UserOutput:
    try:
        return await user_service.get_user_by_id(session=session, user_id=user_id)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
