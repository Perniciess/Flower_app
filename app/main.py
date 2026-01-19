import re
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text
from starlette.middleware.cors import CORSMiddleware
from starlette_csrf import CSRFMiddleware

from app.core.config import settings
from app.core.exceptions import (
    InsufficientPermission,
    PasswordsDoNotMatchError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.core.handlers import (
    insufficient_permission,
    password_not_match_handler,
    user_exists_handler,
    user_not_found_handler,
)
from app.database.session import engine
from app.modules.auth.router import auth_router
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


app = FastAPI(lifespan=lifespan)

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
    secret=settings.CSRF_SECRET_KEY,
    cookie_name=settings.CSRF_COOKIE_NAME,
    header_name=settings.CSRF_HEADER_NAME,
    cookie_secure=settings.COOKIE_SECURE,
    cookie_samesite="strict",
    sensitive_cookies={"access_token"},
    exempt_urls=[
        re.compile(r"^/docs.*"),
        re.compile(r"^/redoc.*"),
        re.compile(r"^/openapi.json"),
        re.compile(r"^/auth/token$"),
        re.compile(r"^/auth/refresh$"),
    ],
)

app.include_router(user_router)
app.include_router(auth_router)

app.add_exception_handler(UserNotFoundError, user_not_found_handler)
app.add_exception_handler(UserAlreadyExistsError, user_exists_handler)
app.add_exception_handler(PasswordsDoNotMatchError, password_not_match_handler)
app.add_exception_handler(InsufficientPermission, insufficient_permission)
