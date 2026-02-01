from pathlib import Path

from fastapi import UploadFile
from pydantic_extra_types.phone_numbers import PhoneNumber

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB

ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}

ALLOWED_IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}


def normalize_phone(v: PhoneNumber) -> str:
    s = str(v)
    if s.startswith("tel:"):
        s = s[4:]
    return s.replace(" ", "").replace("-", "")


def validate_image(image: UploadFile) -> str:
    """Валидирует загружаемое изображение и возвращает расширение файла."""
    if not image.filename:
        raise ValueError("Файл без имени")

    ext = Path(image.filename).suffix.lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValueError(f"Недопустимое расширение файла: {ext}")

    if image.content_type not in ALLOWED_IMAGE_TYPES:
        raise ValueError(f"Недопустимый тип файла: {image.content_type}")

    size = image.size
    if size is not None and size > MAX_IMAGE_SIZE:
        raise ValueError(f"Размер файла {size} байт превышает лимит {MAX_IMAGE_SIZE} байт")

    return ext


def password_strip_and_validate(v: str) -> str:
    v = v.strip()

    if len(v) < 8:
        raise ValueError("Пароль должен быть минимум 8 символов")
    if not any(c.isdigit() for c in v):
        raise ValueError("Пароль должен содержать хотя бы одну цифру")
    if not any(c.islower() for c in v):
        raise ValueError("Пароль должен содержать хотя бы одну строчную букву")
    if not any(c.isupper() for c in v):
        raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")
    if not any(not c.isalnum() for c in v):
        raise ValueError("Пароль должен содержать хотя бы один спецсимвол")
    return v
