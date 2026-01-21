from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class FlowerBase(BaseModel):
    name: str = Field(..., description="Название цветка")
    price: Decimal = Field(..., description="Стоимость цветка")
    description: str = Field(..., description="Описание")
    color: str = Field(..., description="Цвет")


class FlowerCreate(FlowerBase):
    pass


class FlowerUpdate(FlowerBase):
    pass


class FlowerResponse(FlowerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Уникальный идентификатор цветка")
