from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.auth_schemas import UserLogin, UserRegister
from app.schemas.user_schemas import UserOutput
from app.services import auth_service

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", response_model=UserOutput)
async def register(data: UserRegister, session: AsyncSession = Depends(get_db)) -> UserOutput:
    user = await auth_service.register(session=session, data=data)
    return user


@auth_router.post("/login", response_model=UserOutput)
async def login(data: UserLogin, session: AsyncSession = Depends(get_db)) -> UserOutput:
    user = await auth_service.login(session=session, data=data)
    return user
