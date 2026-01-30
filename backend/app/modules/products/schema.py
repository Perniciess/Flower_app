from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductImageResponse(BaseModel):
    """Схема для ответа API с изображениями товара."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    url: str
    sort_order: int


class ProductBase(BaseModel):
    """Базовые поля товара, используемые в других схемах."""

    name: str = Field(..., description="Название товара")
    price: Decimal = Field(..., description="Стоимость товара")
    description: str = Field(..., description="Описание")
    color: str = Field(..., description="Цвет")


class ProductCreate(ProductBase):
    """Схема для создания товара."""

    pass


class ProductUpdate(BaseModel):
    """Схема для частичного обновления данных товара."""

    name: str | None = Field(default=None, description="Название товара")
    price: Decimal | None = Field(default=None, description="Стоимость товара")
    description: str | None = Field(default=None, description="Описание")
    color: str | None = Field(default=None, description="Цвет")


class ProductResponse(ProductBase):
    """Схема для ответа API с данными товара."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Уникальный идентификатор товара")
    images: list[ProductImageResponse] = Field(default_factory=list, description="Изображения товара")
