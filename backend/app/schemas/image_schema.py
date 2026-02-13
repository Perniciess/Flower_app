from pydantic import BaseModel, ConfigDict, Field


class ImageCreate(BaseModel):
    """Внутренняя схема для создания записи изображения в БД."""

    path: str = Field(..., max_length=512, description="Путь до файла на сервере")
    hash: str = Field(..., max_length=64, description="Хеш содержимого файла")
    filename: str = Field(..., max_length=255, description="Оригинальное имя файла")


class ImageUpdate(BaseModel):
    """Схема для обновления изображения."""

    path: str | None = Field(
        default=None, max_length=512, description="Путь до изображения"
    )
    hash: str | None = Field(default=None, max_length=64, description="Хеш изображения")
    original_filename: str | None = Field(
        default=None, max_length=255, description="Оригинальное имя файла"
    )


class ImageResponse(BaseModel):
    """Схема для ответа API с изображениями товара."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Идентификатор изображения")
    url: str = Field(..., description="Ссылка на изображение")
    sort_order: int = Field(..., description="Порядок сортировки")
