from fastapi import APIRouter, Cookie, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.database.session import get_db
from app.modules.users.model import User
from app.modules.users.schema import UserResponse

from . import service as auth_service
from .schema import AuthLogin, AuthRegister
from .utils import remove_token, set_token

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", response_model=UserResponse)
async def register(data: AuthRegister, session: AsyncSession = Depends(get_db)) -> UserResponse:
    user = await auth_service.register(session=session, data=data)
    return user


@auth_router.post("/login")
async def login(response: Response, data: AuthLogin, session: AsyncSession = Depends(get_db)) -> dict[str, str]:
    tokens = await auth_service.login(session=session, data=data)
    set_token(response=response, tokens=tokens)
    return {"message": "Успешная авторизация", "email": data.email}


@auth_router.post("/logout")
async def logout(
    response: Response,
    refresh_token: str = Cookie(),
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict[str, str]:
    await auth_service.logout(session=session, refresh_token=refresh_token)
    remove_token(response)
    return {"message": "Выход из системы выполнен"}


@auth_router.post("/refresh")
async def refresh_token(response: Response, refresh_token: str = Cookie(), session: AsyncSession = Depends(get_db)) -> dict[str, str]:
    tokens = await auth_service.refresh_tokens(session=session, refresh_token=refresh_token)
    set_token(response=response, tokens=tokens)
    return {"message": "Успешная замена токенов"}
