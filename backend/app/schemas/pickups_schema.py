from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber

from app.utils.validators.phone import normalize_phone


class PickupPointBase(BaseModel):
    """Базовая схема точки самовывоза."""

    name: str = Field(..., min_length=1, max_length=255, description="Название точки самовывоза")
    address: str = Field(..., min_length=1, max_length=512, description="Полный адрес точки самовывоза")
    phone: PhoneNumber = Field(..., description="Телефон точки самовывоза")
    latitude: Decimal = Field(..., ge=-90, le=90, description="Широта для отображения на карте")
    longitude: Decimal = Field(..., ge=-180, le=180, description="Долгота для отображения на карте")
    working_hours: str | None = Field(None, max_length=255, description="Часы работы точки самовывоза")
    sort_order: int = Field(0, ge=0, description="Порядок сортировки точек самовывоза")

    @field_validator("phone")
    @classmethod
    def normalize_phone_number(cls, v: PhoneNumber) -> str:
        return normalize_phone(v)


class PickupPointCreate(PickupPointBase):
    """Схема для создания точки самовывоза."""

    is_active: bool = Field(True, description="Флаг активности точки самовывоза")


class PickupPointUpdate(BaseModel):
    """Схема для обновления точки самовывоза."""

    name: str | None = Field(None, min_length=1, max_length=255, description="Название точки самовывоза")
    address: str | None = Field(None, min_length=1, max_length=512, description="Полный адрес точки самовывоза")
    phone: PhoneNumber | None = Field(None, description="Телефон точки самовывоза")
    latitude: Decimal | None = Field(None, ge=-90, le=90, description="Широта для отображения на карте")
    longitude: Decimal | None = Field(None, ge=-180, le=180, description="Долгота для отображения на карте")
    working_hours: str | None = Field(None, max_length=255, description="Часы работы точки самовывоза")
    is_active: bool | None = Field(None, description="Флаг активности точки самовывоза")
    sort_order: int | None = Field(None, ge=0, description="Порядок сортировки точек самовывоза")

    @field_validator("phone")
    @classmethod
    def normalize_phone_number(cls, v: PhoneNumber | None) -> str | None:
        if v is not None:
            return normalize_phone(v)
        return v


class PickupPointResponse(PickupPointBase):
    """Схема ответа API с данными точки самовывоза."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Уникальный идентификатор точки самовывоза")
    is_active: bool = Field(..., description="Флаг активности точки самовывоза")
