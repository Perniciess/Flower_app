import re
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.security import APIKeyHeader
from sqlalchemy import text
from starlette.middleware.cors import CORSMiddleware
from starlette_csrf import CSRFMiddleware

from app.core.config import settings
from app.core.exceptions import (
    CartAlreadyExistsException,
    CartItemNotFoundError,
    CartNotFoundError,
    FlowerNotFoundError,
    ImageNotFoundError,
    InsufficientPermission,
    InvalidToken,
    PasswordsDoNotMatchError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.core.handlers import (
    cart_already_exists,
    cart_item_not_found,
    cart_not_found,
    flower_not_found,
    image_not_found,
    insufficient_permission,
    invalid_token,
    password_not_match_handler,
    user_exists_handler,
    user_not_found_handler,
)
from app.database.session import engine
from app.modules.auth.router import auth_router
from app.modules.carts.router import cart_router
from app.modules.flowers.router import flower_router
from app.modules.users.router import user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        print("DB connected")
    except Exception as exc:
        print(f"DB connection failed: {exc}")
    yield
    await engine.dispose()


app = FastAPI(
    title="FlowerShop API",
    description="API для магазина цветов",
    openapi_tags=[
        {"name": "users", "description": "Операции с пользователями"},
        {"name": "auth", "description": "Аутентификация и авторизация"},
        {"name": "flowers", "description": "Операции с цветами"},
        {"name": "carts", "description": "Корзина покупок"},
    ],
    lifespan=lifespan,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

csrf_header_scheme = APIKeyHeader(name=settings.CSRF_HEADER_NAME, auto_error=False)

if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.add_middleware(
    CSRFMiddleware,
    cookie_httponly=False,
    secret=settings.CSRF_SECRET_KEY,
    cookie_name=settings.CSRF_COOKIE_NAME,
    header_name=settings.CSRF_HEADER_NAME,
    cookie_secure=settings.COOKIE_SECURE,
    cookie_samesite="strict",
    sensitive_cookies={"access_token"},
    exempt_urls=[
        re.compile(r"/docs"),
        re.compile(r"/openapi.json"),
        re.compile(r"/auth/login"),
    ],
)

app.include_router(user_router, dependencies=[Depends(csrf_header_scheme)])
app.include_router(auth_router, dependencies=[Depends(csrf_header_scheme)])
app.include_router(flower_router, dependencies=[Depends(csrf_header_scheme)])
app.include_router(cart_router, dependencies=[Depends(csrf_header_scheme)])

app.add_exception_handler(UserNotFoundError, user_not_found_handler)
app.add_exception_handler(UserAlreadyExistsError, user_exists_handler)
app.add_exception_handler(PasswordsDoNotMatchError, password_not_match_handler)
app.add_exception_handler(InsufficientPermission, insufficient_permission)
app.add_exception_handler(InvalidToken, invalid_token)
app.add_exception_handler(FlowerNotFoundError, flower_not_found)
app.add_exception_handler(ImageNotFoundError, image_not_found)
app.add_exception_handler(CartAlreadyExistsException, cart_already_exists)
app.add_exception_handler(CartNotFoundError, cart_not_found)
app.add_exception_handler(CartItemNotFoundError, cart_item_not_found)
