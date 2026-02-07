from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductImageResponse(BaseModel):
    """Схема для ответа API с изображениями товара."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    url: str
    sort_order: int


class FlowerInComposition(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: Decimal


class ProductBase(BaseModel):
    name: str = Field(..., max_length=255, description="Название товара")
    price: Decimal = Field(..., gt=0, description="Стоимость товара")
    description: str = Field(..., max_length=2000, description="Описание")
    color: str = Field(..., max_length=64, description="Цвет")
    is_active: bool = Field(default=True, description="Активен ли товар")
    in_stock: bool = Field(default=True, description="В наличии")


class ProductCreate(ProductBase):
    """Схема для создания товара."""

    pass


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255, description="Название товара")
    price: Decimal | None = Field(default=None, gt=0, description="Стоимость товара")
    description: str | None = Field(default=None, max_length=2000, description="Описание")
    color: str | None = Field(default=None, max_length=64, description="Цвет")
    is_active: bool | None = Field(default=None, description="Активен ли товар")
    in_stock: bool | None = Field(default=None, description="В наличии")


class ProductResponse(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Уникальный идентификатор товара")
    images: list[ProductImageResponse] = Field(default_factory=list, description="Изображения товара")
    composition: list[FlowerInComposition] = Field(default_factory=list, description="Состав букета")
    discounted_price: Decimal | None = Field(default=None, description="Цена со скидкой")
    discount_percentage: Decimal | None = Field(default=None, description="Процент скидки")
