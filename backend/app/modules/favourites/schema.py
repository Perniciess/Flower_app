from pydantic import BaseModel, ConfigDict, Field

from app.modules.products.schema import ProductResponse


class FavouriteBase(BaseModel):
    """Базовая схема избранного."""

    product_id: int = Field(..., description="ID товара")


class FavouriteResponse(BaseModel):
    """Схема ответа с информацией об избранном товаре."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="ID записи в избранном")
    product: ProductResponse = Field(..., description="Информация о товаре")
