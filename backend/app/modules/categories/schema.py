import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CategoryBase(BaseModel):
    name: str = Field(
        ..., description="Название категории", min_length=1, max_length=255
    )
    slug: str = Field(
        ...,
        description="URL-friendly идентификатор категории",
        min_length=1,
        max_length=255,
    )
    description: str | None = Field(default=None, description="Описание категории")
    image_url: str | None = Field(default=None, description="URL изображения категории")
    parent_id: int | None = Field(default=None, description="ID родительской категории")
    sort_order: int = Field(default=0, description="Порядок сортировки")

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: str) -> str:
        v = v.lower().strip()

        if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", v):
            raise ValueError(
                "Slug может содержать только строчные латинские буквы, цифры и дефисы. "
                "Дефис не может быть в начале или конце."
            )

        return v


class CategoryCreate(CategoryBase):
    is_active: bool = Field(default=False, description="Статус активности категории")


class CategoryUpdate(BaseModel):
    name: str | None = Field(
        default=None, description="Название категории", min_length=1, max_length=255
    )
    slug: str | None = Field(
        default=None,
        description="URL-friendly идентификатор категории",
        min_length=1,
        max_length=255,
    )
    description: str | None = Field(default=None, description="Описание категории")
    image_url: str | None = Field(default=None, description="URL изображения категории")
    parent_id: int | None = Field(default=None, description="ID родительской категории")
    is_active: bool | None = Field(
        default=None, description="Статус активности категории"
    )
    sort_order: int | None = Field(default=None, description="Порядок сортировки")

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: str | None) -> str | None:
        if v is None:
            return v

        v = v.lower().strip()

        if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", v):
            raise ValueError(
                "Slug может содержать только строчные латинские буквы, цифры и дефисы. "
                "Дефис не может быть в начале или конце."
            )

        return v


class CategoryResponse(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Уникальный идентификатор категории")
    is_active: bool = Field(..., description="Статус активности категории")
    created_at: datetime = Field(..., description="Дата создания")
    updated_at: datetime = Field(..., description="Дата последнего обновления")


class CategoryWithChildren(CategoryResponse):
    children: list["CategoryWithChildren"] = Field(
        default_factory=list, description="Подкатегории"
    )


CategoryWithChildren.model_rebuild()
