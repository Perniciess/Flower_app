import asyncio

from fastapi import (
    APIRouter,
    Depends,
    Path,
    Request,
    Response,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.deps import get_current_user, verify_bot_api_key
from app.core.limiter import limiter
from app.core.redis import get_redis
from app.core.security import oauth2_scheme
from app.db.session import get_db
from app.models.users_model import User
from app.schemas.auth_schema import (
    AccessToken,
    AuthChangePassword,
    AuthLogin,
    AuthPhone,
    AuthRegister,
    AuthSetNewPassword,
    VerificationDeepLink,
)
from app.service import auth_service
from app.utils.cookie import get_refresh_cookie_settings, remove_token, set_token

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post(
    "/register",
    response_model=VerificationDeepLink,
    status_code=status.HTTP_201_CREATED,
    summary="Зарегистрироваться",
)
@limiter.limit("3/minute")
async def register(
    request: Request,
    data: AuthRegister,
    redis: Redis = Depends(get_redis),
    session: AsyncSession = Depends(get_db),
) -> VerificationDeepLink:
    """Регистрация пользователя."""
    return await auth_service.register(session=session, redis=redis, data=data)


@auth_router.post(
    "/login",
    response_model=AccessToken,
    status_code=status.HTTP_200_OK,
    summary="Авторизоваться",
)
@limiter.limit("5/minute")
async def login(
    request: Request,
    response: Response,
    data: AuthLogin,
    redis: Redis = Depends(get_redis),
    session: AsyncSession = Depends(get_db),
) -> AccessToken:
    """Авторизация пользователя."""
    tokens = await auth_service.login(session=session, redis=redis, data=data)
    set_token(response=response, tokens=tokens)
    return AccessToken(access_token=tokens.access_token)


@limiter.limit("10/minute")
@auth_router.post(
    "/logout",
    response_model=dict[str, str],
    status_code=status.HTTP_200_OK,
    summary="Выйти из системы",
)
async def logout(
    request: Request,
    response: Response,
    redis: Redis = Depends(get_redis),
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    header_token: str | None = Depends(oauth2_scheme),
) -> dict[str, str]:
    """
    Выйти из системы.

    Требует авторизации.
    """
    refresh_token = request.cookies.get(get_refresh_cookie_settings()["key"], "")
    await auth_service.logout(
        session=session,
        redis=redis,
        access_token=header_token or "",
        refresh_token=refresh_token,
    )
    remove_token(response)
    return {"message": "Выход из системы выполнен"}


@auth_router.post(
    "/refresh",
    response_model=AccessToken,
    status_code=status.HTTP_200_OK,
    summary="Обновить токены",
)
@limiter.limit("10/minute")
async def refresh_token(
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_db),
) -> AccessToken:
    """
    Обновить токены.

    Требует авторизации.
    """
    rt = request.cookies.get(get_refresh_cookie_settings()["key"], "")
    tokens = await auth_service.refresh_tokens(session=session, refresh_token=rt)
    set_token(response=response, tokens=tokens)
    return AccessToken(access_token=tokens.access_token)


@auth_router.post(
    "/complete-register/{verification_token}",
    response_model=dict[str, str],
    status_code=status.HTTP_200_OK,
    summary="Завершение регистрации",
)
@limiter.limit("3/minute")
async def complete_register(
    request: Request,
    verification_token: str = Path(max_length=128),
    redis: Redis = Depends(get_redis),
    session: AsyncSession = Depends(get_db),
    _bot_auth: None = Depends(verify_bot_api_key),
) -> dict[str, str]:
    """Завершить регистрацию после подтверждения номера в телеграме."""
    await auth_service.complete_register(
        session=session, redis=redis, verification_token=verification_token
    )
    return {"message": "Успешная регистрация"}


@limiter.limit("5/minute")
@auth_router.post(
    "/change-password",
    response_model=AccessToken,
    status_code=status.HTTP_200_OK,
    summary="Смена пароля",
)
async def change_password(
    request: Request,
    response: Response,
    data: AuthChangePassword,
    redis: Redis = Depends(get_redis),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
    header_token: str | None = Depends(oauth2_scheme),
) -> AccessToken:
    """
    Изменить пароль пользователя.

    Требует авторизации.
    """
    remove_token(response=response)
    tokens = await auth_service.change_password(
        session=session,
        redis=redis,
        access_token=header_token or "",
        user_id=current_user.id,
        data=data,
    )
    set_token(response=response, tokens=tokens)
    return AccessToken(access_token=tokens.access_token)


@auth_router.post(
    "/reset_password", status_code=status.HTTP_200_OK, summary="Сброс пароля"
)
@limiter.limit("3/hour")
async def reset_password(
    request: Request,
    data: AuthPhone,
    redis: Redis = Depends(get_redis),
    session: AsyncSession = Depends(get_db),
) -> VerificationDeepLink:
    """
    Сбросить пароля пользователя с подтверждением в ТГ.
    """
    return await auth_service.reset_password(
        session=session, redis=redis, phone_number=data.phone_number
    )


@auth_router.post(
    "/complete-reset-verification/{reset_token}",
    response_model=dict[str, str],
    status_code=status.HTTP_200_OK,
    summary="Завершение сброса пароля",
)
@limiter.limit("3/minute")
async def complete_reset(
    request: Request,
    reset_token: str = Path(max_length=128),
    redis: Redis = Depends(get_redis),
    _bot_auth: None = Depends(verify_bot_api_key),
) -> dict[str, str]:
    """
    Завершить сброс пароля пользователя.
    """
    await auth_service.complete_reset(redis=redis, reset_token=reset_token)
    return {"message": "Верификация пройдена"}


@auth_router.websocket("/ws/reset/{reset_token}")
async def reset_websocket(
    reset_token: str = Path(max_length=128),
    *,
    websocket: WebSocket,
    redis: Redis = Depends(get_redis),
):
    """
    Установить ws-соединение для уведомления фронтенда об сбросе пароля.
    """
    origin = websocket.headers.get("origin")
    allowed_origins = settings.all_cors_origins
    if origin not in allowed_origins:
        await websocket.close(code=1008, reason="Origin not allowed")
        return

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
            message = await pubsub.get_message(
                ignore_subscribe_messages=True, timeout=1.0
            )
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


@limiter.limit("3/minute")
@auth_router.post(
    "/set-new-password",
    response_model=AccessToken,
    status_code=status.HTTP_200_OK,
    summary="Установка нового пароля",
)
async def set_new_password(
    request: Request,
    data: AuthSetNewPassword,
    response: Response,
    redis: Redis = Depends(get_redis),
    session: AsyncSession = Depends(get_db),
) -> AccessToken:
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
    return AccessToken(access_token=tokens.access_token)
