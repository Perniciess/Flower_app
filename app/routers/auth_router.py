from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.auth_schemas import Token, UserLogin, UserRegister
from app.schemas.user_schemas import UserOutput
from app.services import auth_service

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", response_model=UserOutput)
async def register(data: UserRegister, session: AsyncSession = Depends(get_db)) -> UserOutput:
    user = await auth_service.register(session=session, data=data)
    return user


@auth_router.post("/login", response_model=Token)
async def login(data: UserLogin, session: AsyncSession = Depends(get_db)) -> Token:
    user_token = await auth_service.login(session=session, data=data)
    return user_token


@auth_router.post("/token", response_model=Token)
async def token(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_db)) -> Token:
    data = UserLogin(email=form_data.username, password=form_data.password)
    return await auth_service.login(session=session, data=data)
