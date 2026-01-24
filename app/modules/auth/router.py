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


@auth_router.post("/register", response_model=UserResponse, summary="Зарегистрироваться")
async def register(data: AuthRegister, session: AsyncSession = Depends(get_db)) -> UserResponse:
    """Регистрация пользователя."""
    user = await auth_service.register(session=session, data=data)
    return user


@auth_router.post("/login", summary="Авторизоваться")
async def login(response: Response, data: AuthLogin, session: AsyncSession = Depends(get_db)) -> dict[str, str]:
    """Авторизация пользователя."""
    tokens = await auth_service.login(session=session, data=data)
    set_token(response=response, tokens=tokens)
    return {"message": "Успешная авторизация", "phone_number": data.phone_number}


@auth_router.post("/logout", summary="Выйти из системы")
async def logout(
    response: Response,
    refresh_token: str = Cookie(),
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict[str, str]:
    """
    Выход из системы.

    Необходимо быть авторизованным в системе.
    """
    await auth_service.logout(session=session, refresh_token=refresh_token)
    remove_token(response)
    return {"message": "Выход из системы выполнен"}


@auth_router.post("/refresh", summary="Обновить токены")
async def refresh_token(response: Response, refresh_token: str = Cookie(), session: AsyncSession = Depends(get_db)) -> dict[str, str]:
    """Обновление токенов."""
    tokens = await auth_service.refresh_tokens(session=session, refresh_token=refresh_token)
    set_token(response=response, tokens=tokens)
    return {"message": "Успешная замена токенов"}
