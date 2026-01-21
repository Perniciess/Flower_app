from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class FlowerImageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    url: str
    sort_order: int


class FlowerBase(BaseModel):
    name: str = Field(..., description="Название цветка")
    price: Decimal = Field(..., description="Стоимость цветка")
    description: str = Field(..., description="Описание")
    color: str = Field(..., description="Цвет")


class FlowerCreate(FlowerBase):
    pass


class FlowerUpdate(BaseModel):
    name: str | None = Field(default=None, description="Название цветка")
    price: Decimal | None = Field(default=None, description="Стоимость цветка")
    description: str | None = Field(default=None, description="Описание")
    color: str | None = Field(default=None, description="Цвет")


class FlowerResponse(FlowerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Уникальный идентификатор цветка")
    images: list[FlowerImageResponse] = Field(default_factory=list, description="Изображения цветка")
