from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class FlowerImageResponse(BaseModel):
    """Схема ответа API с изображениями цветка."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    url: str
    sort_order: int


class FlowerBase(BaseModel):
    """Базовые поля цветка, используемые в других схемах."""

    name: str = Field(..., description="Название цветка")
    price: Decimal = Field(..., description="Стоимость цветка")
    description: str = Field(..., description="Описание")
    color: str = Field(..., description="Цвет")


class FlowerCreate(FlowerBase):
    """Схема для создания цветка."""

    pass


class FlowerUpdate(BaseModel):
    """Схема для частичного обновления данных цветка."""

    name: str | None = Field(default=None, description="Название цветка")
    price: Decimal | None = Field(default=None, description="Стоимость цветка")
    description: str | None = Field(default=None, description="Описание")
    color: str | None = Field(default=None, description="Цвет")


class FlowerResponse(FlowerBase):
    """Схема ответа API с данными цветка."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Уникальный идентификатор цветка")
    images: list[FlowerImageResponse] = Field(default_factory=list, description="Изображения цветка")
