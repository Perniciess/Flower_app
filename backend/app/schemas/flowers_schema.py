from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class FlowerCreate(BaseModel):
    name: str = Field(..., description="Название цветка")
    price: Decimal = Field(..., ge=0, description="Цена за штуку")


class FlowerUpdate(BaseModel):
    name: str | None = Field(default=None, description="Название цветка")
    price: Decimal | None = Field(default=None, ge=0, description="Цена за штуку")


class FlowerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Уникальный идентификатор")
    name: str = Field(..., description="Название цветка")
    price: Decimal = Field(..., description="Цена за штуку")


class CompositionItem(BaseModel):
    flower_id: int = Field(..., description="ID цветка")
    quantity: int = Field(..., ge=1, description="Количество")


class SetCompositionRequest(BaseModel):
    items: list[CompositionItem] = Field(..., description="Состав букета")
