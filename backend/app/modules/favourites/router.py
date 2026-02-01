from collections.abc import Sequence

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_client
from app.database.session import get_db
from app.modules.users.model import User

from . import service as favourite_service
from .schema import FavouriteResponse

favourite_router = APIRouter(prefix="/favourite", tags=["favourite"])


@favourite_router.post("/add/{product_id}", response_model=FavouriteResponse, status_code=status.HTTP_201_CREATED, summary="Добавить товар в избранное")
async def add_to_favourite(
    product_id: int, session: AsyncSession = Depends(get_db), current_user: User = Depends(require_client)
) -> FavouriteResponse:
    """
    Добавить товар в избранное.

    Требует авторизации.
    """
    favourite = await favourite_service.add_to_favourite(
        session=session, product_id=product_id, user_id=current_user.id
    )
    return favourite


@favourite_router.get("/list", response_model=Sequence[FavouriteResponse], status_code=status.HTTP_200_OK, summary="Получить список избранных товаров")
async def get_favourite_list(
    session: AsyncSession = Depends(get_db), current_user: User = Depends(require_client)
) -> Sequence[FavouriteResponse]:
    """
    Получить список избранных товаров пользователя.

    Требует авторизации.
    """
    favourites = await favourite_service.get_favourite_list(session=session, user_id=current_user.id)
    return favourites


@favourite_router.delete("/delete/{product_id}", response_model=dict[str, str], status_code=status.HTTP_200_OK, summary="Удалить товар из избранных")
async def delete_from_favourites(
    product_id: int, session: AsyncSession = Depends(get_db), current_user: User = Depends(require_client)
):
    """
    Удалить товар из избранных.

    Требует авторизации.
    """
    await favourite_service.delete_from_favourites(session=session, product_id=product_id, user_id=current_user.id)
    return {"message": "Успешно удалено из избранных"}
