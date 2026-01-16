from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.core.exceptions import UserAlreadyExistsError, UserNotFoundError
from app.core.handlers import user_exists_handler, user_not_found_handler
from app.database.session import engine
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
app.add_exception_handler(UserNotFoundError, user_not_found_handler)
app.add_exception_handler(UserAlreadyExistsError, user_exists_handler)
