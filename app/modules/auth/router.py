from fastapi import APIRouter, Cookie, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.modules.users.schema import UserOutput

from . import service as auth_service
from .schema import UserLogin, UserRegister
from .utils import remove_token, set_token

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", response_model=UserOutput)
async def register(data: UserRegister, session: AsyncSession = Depends(get_db)) -> UserOutput:
    user = await auth_service.register(session=session, data=data)
    return user


@auth_router.post("/login")
async def login(response: Response, data: UserLogin, session: AsyncSession = Depends(get_db)) -> dict[str, str]:
    tokens = await auth_service.login(session=session, data=data)
    set_token(response=response, tokens=tokens)
    return {"message": "Успешная авторизация", "email": data.email}


@auth_router.post("/logout")
async def logout(response: Response, refresh_token: str = Cookie(), session: AsyncSession = Depends(get_db)):
    await auth_service.logout(session=session, refresh_token=refresh_token)
    remove_token(response)
    return {"message": "Выход из системы выполнен"}


@auth_router.post("/refresh")
async def refresh_token(response: Response, refresh_token: str = Cookie(), session: AsyncSession = Depends(get_db)):
    tokens = await auth_service.refresh_tokens(session=session, refresh_token=refresh_token)
    set_token(response=response, tokens=tokens)
    return {"message": "Успешная замена токенов"}
