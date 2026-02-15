import json
from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    field_validator,
    model_validator,
)

from app.utils.validators.link import validate_link_scheme

from .image_schema import ImageResponse


class BannerBase(BaseModel):
    title: str = Field(..., max_length=255, description="Заголовок баннера")
    description: str | None = Field(
        default=None, max_length=200, description="Краткое описание баннера"
    )
    link: str | None = Field(
        default=None, max_length=512, description="Ссылка при клике"
    )

    sort_order: int = Field(default=0, description="Порядок сортировки")
    is_active: bool = Field(default=False, description="Активен ли баннер")

    @model_validator(mode="before")
    @classmethod
    def parse_json_string(cls, data: Any) -> Any:
        if isinstance(data, str):
            return json.loads(data)
        return data

    @field_validator("link")
    @classmethod
    def validate_link_scheme(cls, v: str | None) -> str | None:
        return validate_link_scheme(v)


class BannerCreate(BannerBase):
    pass


class BannerUpdate(BaseModel):
    title: str | None = Field(
        default=None, max_length=255, description="Заголовок баннера"
    )
    description: str | None = Field(
        default=None, max_length=200, description="Краткое описание баннера"
    )
    link: str | None = Field(
        default=None, max_length=512, description="Ссылка при клике"
    )
    sort_order: int | None = Field(default=None, description="Порядок сортировки")
    is_active: bool | None = Field(default=None, description="Активен ли баннер")

    @model_validator(mode="before")
    @classmethod
    def parse_json_string(cls, data: Any) -> Any:
        if isinstance(data, str):
            return json.loads(data)
        return data

    @field_validator("link")
    @classmethod
    def validate_link_scheme(cls, v: str | None) -> str | None:
        return validate_link_scheme(v)


class BannerResponse(BannerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Уникальный идентификатор")

    image: ImageResponse | None = Field(default=None, exclude=True)

    @computed_field
    @property
    def image_url(self) -> str | None:
        return self.image.path if self.image else None
