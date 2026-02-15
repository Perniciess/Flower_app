from pydantic import BaseModel, ConfigDict, Field


class ImageCreate(BaseModel):
    path: str = Field(..., max_length=512, description="Путь до файла на сервере")
    hash: str = Field(..., max_length=64, description="Хеш содержимого файла")
    original_filename: str = Field(
        ..., max_length=255, description="Оригинальное имя файла"
    )


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
    model_config = ConfigDict(from_attributes=True)

    id: int
    path: str = Field(..., max_length=512, description="Путь до файла на сервере")
