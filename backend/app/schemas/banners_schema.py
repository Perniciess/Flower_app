from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.utils.validators.link import validate_link_scheme


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

    @field_validator("link")
    @classmethod
    def validate_link_scheme(cls, v: str | None) -> str | None:
        return validate_link_scheme(v)


class BannerResponse(BannerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Уникальный идентификатор")
    image_url: str | None = Field(default=None, description="URL изображения")
