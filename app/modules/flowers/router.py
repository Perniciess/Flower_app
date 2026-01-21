from collections.abc import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db

from . import service as flower_service
from .schema import FlowerCreate, FlowerResponse

flower_router = APIRouter(prefix="/flowers", tags=["flowers"])


@flower_router.post("/create", response_model=FlowerResponse)
async def create_flower(data: FlowerCreate, session: AsyncSession = Depends(get_db)) -> FlowerResponse:
    flower = await flower_service.create_flower(session=session, flower_data=data)
    return flower


@flower_router.get("/", response_model=Sequence[FlowerResponse])
async def get_flowers(session: AsyncSession = Depends(get_db)) -> Sequence[FlowerResponse]:
    flowers = await flower_service.get_flowers(session=session)
    return flowers

@flower_router.patch("/{flower_id}", response_model=)
