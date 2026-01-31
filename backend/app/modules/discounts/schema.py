from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class DiscountBase(BaseModel):
    name: str = Field(..., description="Название акции")
    product_id: int | None = Field(default=None, description="Уникальный идентификатор товара")
    category_id: int | None = Field(default=None, description="Уникальный идентификатор категории")
    percentage: Decimal | None = Field(default=None, ge=0, le=100, description="Процент скидки")
    new_price: Decimal | None = Field(default=None, ge=0, description="Новая цена товара")
    is_active: bool = Field(default=True, description="Активна ли акция сейчас")


class DiscountCreate(DiscountBase):
    @model_validator(mode="after")
    def validate_target_and_value(self) -> "DiscountCreate":
        has_product = self.product_id is not None
        has_category = self.category_id is not None
        if has_product == has_category:
            raise ValueError("Укажите ровно одно из полей: product_id или category_id")

        has_percentage = self.percentage is not None
        has_new_price = self.new_price is not None
        if has_percentage == has_new_price:
            raise ValueError("Укажите ровно одно из полей: percentage или new_price")

        if has_category and has_new_price:
            raise ValueError("Для скидки на категорию нельзя указать new_price, используйте percentage")

        return self


class DiscountUpdate(BaseModel):
    name: str | None = Field(default=None, description="Название акции")
    percentage: Decimal | None = Field(default=None, ge=0, le=100, description="Процент скидки")
    new_price: Decimal | None = Field(default=None, ge=0, description="Новая цена товара")
    is_active: bool | None = Field(default=None, description="Активна ли акция сейчас")


class DiscountResponse(DiscountBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Уникальный идентификатор акции")
    discount_type: str = Field(..., description="Тип скидки")


class DiscountBrief(BaseModel):
    percentage: Decimal | None
    new_price: Decimal | None
