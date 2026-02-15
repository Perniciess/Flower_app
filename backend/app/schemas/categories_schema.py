from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.utils.validators.slug import validate_slug


class CategoryBase(BaseModel):
    """Базовые поля категории, используемые в других схемах."""

    name: str = Field(
        ..., description="Название категории", min_length=1, max_length=255
    )
    slug: str = Field(
        ...,
        description="URL-friendly идентификатор категории",
        min_length=1,
        max_length=255,
    )
    description: str | None = Field(
        default=None, max_length=2000, description="Описание категории"
    )
    parent_id: int | None = Field(default=None, description="ID родительской категории")
    sort_order: int = Field(default=0, description="Порядок сортировки")

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: str) -> str:
        return validate_slug(v)


class CategoryCreate(CategoryBase):
    """Схема для создания категории."""

    is_active: bool = Field(default=False, description="Статус активности категории")


class CategoryUpdate(BaseModel):
    """Схема для обновление категории."""

    name: str | None = Field(
        default=None, description="Название категории", min_length=1, max_length=255
    )
    slug: str | None = Field(
        default=None,
        description="URL-friendly идентификатор категории",
        min_length=1,
        max_length=255,
    )
    description: str | None = Field(
        default=None, max_length=2000, description="Описание категории"
    )
    parent_id: int | None = Field(default=None, description="ID родительской категории")
    is_active: bool | None = Field(
        default=None, description="Статус активности категории"
    )
    sort_order: int | None = Field(default=None, description="Порядок сортировки")

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: str) -> str:
        return validate_slug(v)


class CategoryResponse(CategoryBase):
    """Схема ответа API ответа с информацией о категории."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Уникальный идентификатор категории")
    is_active: bool = Field(..., description="Статус активности категории")
    image_id: int | None = Field(default=None, description="ID изображения")
    created_at: datetime = Field(..., description="Дата создания")
    updated_at: datetime = Field(..., description="Дата последнего обновления")


class CategoryWithChildren(CategoryResponse):
    """Схема ответа API ответа об древовидной структура категорий."""

    children: list["CategoryWithChildren"] = Field(
        default_factory=list, description="Подкатегории"
    )


CategoryWithChildren.model_rebuild()
