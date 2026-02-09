from pydantic import BaseModel, ConfigDict, Field


class BannerCreate(BaseModel):
    title: str | None = Field(
        default=None, max_length=255, description="Заголовок баннера"
    )
    description: str | None = Field(
        default=None, max_length=200, description="Краткое описание баннера"
    )
    link: str | None = Field(
        default=None, max_length=512, description="Ссылка при клике"
    )
    sort_order: int = Field(default=0, description="Порядок сортировки")
    is_active: bool = Field(default=True, description="Активен ли баннер")


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


class BannerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Уникальный идентификатор")
    title: str | None = Field(default=None, description="Заголовок баннера")
    description: str | None = Field(
        default=None, description="Краткое описание баннера"
    )
    image_url: str | None = Field(default=None, description="URL изображения")
    link: str | None = Field(default=None, description="Ссылка при клике")
    sort_order: int = Field(..., description="Порядок сортировки")
    is_active: bool = Field(..., description="Активен ли баннер")
