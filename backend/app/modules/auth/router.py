import asyncio

from fastapi import APIRouter, Cookie, Depends, Response, WebSocket, WebSocketDisconnect
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.core.redis import get_redis
from app.database.session import get_db
from app.modules.users.model import User

from . import service as auth_service
from .schema import (
    AuthChangePassword,
    AuthLogin,
    AuthPhone,
    AuthRegister,
    AuthSetNewPassword,
    VerificationDeepLink,
)
from .utils import remove_token, set_token

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", response_model=VerificationDeepLink, summary="Зарегистрироваться")
async def register(
    data: AuthRegister,
    redis: Redis = Depends(get_redis),
    session: AsyncSession = Depends(get_db),
) -> VerificationDeepLink:
    """Регистрация пользователя."""
    return await auth_service.register(session=session, redis=redis, data=data)


@auth_router.post("/login", summary="Авторизоваться")
async def login(response: Response, data: AuthLogin, session: AsyncSession = Depends(get_db)) -> dict[str, str]:
    """Авторизация пользователя."""
    tokens = await auth_service.login(session=session, data=data)
    set_token(response=response, tokens=tokens)
    return {"message": "Успешная авторизация", "phone_number": data.phone_number}


@auth_router.post("/logout", summary="Выйти из системы")
async def logout(
    response: Response,
    access_token: str = Cookie(),
    refresh_token: str = Cookie(),
    redis: Redis = Depends(get_redis),
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict[str, str]:
    """
    Выйти из системы.

    Требует авторизации.
    """
    await auth_service.logout(
        session=session,
        redis=redis,
        access_token=access_token,
        refresh_token=refresh_token,
    )
    remove_token(response)
    return {"message": "Выход из системы выполнен"}


@auth_router.post("/refresh", summary="Обновить токены")
async def refresh_token(
    response: Response,
    refresh_token: str = Cookie(),
    session: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    """
    Обновить токены.

    Требует авторизации.
    """
    tokens = await auth_service.refresh_tokens(session=session, refresh_token=refresh_token)
    set_token(response=response, tokens=tokens)
    return {"message": "Успешная замена токенов"}


@auth_router.post("/complete-register/{verification_token}", summary="Завершение регистрации")
async def complete_register(
    verification_token: str,
    redis: Redis = Depends(get_redis),
    session: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    """Завершить регистрацию после подтверждения номера в телеграме."""
    await auth_service.complete_register(session=session, redis=redis, verification_token=verification_token)
    return {"message": "Успешная регистрация"}


@auth_router.post("/change-password", summary="Смена пароля")
async def change_password(
    response: Response,
    data: AuthChangePassword,
    redis: Redis = Depends(get_redis),
    access_token: str = Cookie(),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    """
    Изменить пароль пользователя.

    Требует авторизации.
    """
    remove_token(response=response)
    tokens = await auth_service.change_password(
        session=session,
        redis=redis,
        access_token=access_token,
        user_id=current_user.id,
        data=data,
    )
    set_token(response=response, tokens=tokens)
    return {"message": "Успешная смена пароля"}


@auth_router.post("/reset_password", summary="Сброс пароля")
async def reset_password(
    data: AuthPhone,
    redis: Redis = Depends(get_redis),
    session: AsyncSession = Depends(get_db),
) -> VerificationDeepLink:
    """
    Сбросить пароля пользователя с подтверждением в ТГ.
    """
    return await auth_service.reset_password(session=session, redis=redis, phone_number=data.phone_number)


@auth_router.post("/complete-reset-verification/{reset_token}")
async def complete_reset(reset_token: str, redis: Redis = Depends(get_redis)) -> dict[str, str]:
    """
    Завершить сброс пароля пользователя.
    """
    await auth_service.complete_reset(redis=redis, reset_token=reset_token)
    return {"message": "Верификация пройдена"}


@auth_router.websocket("/ws/reset/{reset_token}")
async def reset_websocket(reset_token: str, websocket: WebSocket, redis: Redis = Depends(get_redis)):
    """
    Установить ws-соединение для уведомления фронтенда об сбросе пароля.
    """
    redis_data = await redis.get(f"r:{reset_token}")
    if redis_data is None:
        await websocket.accept()
        await websocket.close(code=1008, reason="Invalid token")
        return

    ttl = await redis.ttl(f"r:{reset_token}")
    await websocket.accept()

    pubsub = redis.pubsub()
    await pubsub.subscribe(f"reset:{reset_token}")
    try:
        deadline = asyncio.get_running_loop().time() + ttl
        while asyncio.get_running_loop().time() < deadline:
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if message and message["type"] == "message":
                await websocket.send_json({"verified": True})
                await websocket.close()
                return
        await websocket.close(code=1000, reason="Timeout")
    except WebSocketDisconnect:
        pass
    finally:
        await pubsub.unsubscribe(f"reset:{reset_token}")
        await pubsub.aclose()


@auth_router.post("/set-new-password", summary="Установка нового пароля")
async def set_new_password(
    data: AuthSetNewPassword,
    response: Response,
    redis: Redis = Depends(get_redis),
    session: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    """
    Установить новый пароль после уведомления на фронтенд и получения с него пароля.
    """
    tokens = await auth_service.set_new_password(
        session=session,
        redis=redis,
        reset_token=data.reset_token,
        new_password=data.new_password,
    )
    set_token(response=response, tokens=tokens)
    return {"message": "Успешный сброс пароля!"}
