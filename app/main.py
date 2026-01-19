from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

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
from app.routers.auth_router import auth_router
from app.routers.user_router import user_router


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
app.include_router(user_router)
app.include_router(auth_router)

app.add_exception_handler(UserNotFoundError, user_not_found_handler)
app.add_exception_handler(UserAlreadyExistsError, user_exists_handler)
app.add_exception_handler(PasswordsDoNotMatchError, password_not_match_handler)
app.add_exception_handler(InsufficientPermission, insufficient_permission)
