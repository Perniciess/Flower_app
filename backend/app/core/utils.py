from pathlib import Path

import magic
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
    """
    Валидирует загружаемое изображение:
    1. Проверяет расширение.
    2. Проверяет размер.
    3. Проверяет реальный MIME-тип через сигнатуру файла (Magic Numbers).
    """
    if not image.filename:
        raise ValueError("Файл без имени")

    ext = Path(image.filename).suffix.lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValueError(f"Недопустимое расширение файла: {ext}")

    if image.size is not None and image.size > MAX_IMAGE_SIZE:
        raise ValueError(f"Размер файла превышает лимит {MAX_IMAGE_SIZE // (1024 * 1024)} MB")

    header = image.file.read(2048)
    image.file.seek(0)

    actual_mime = magic.from_buffer(header, mime=True)
    if actual_mime not in ALLOWED_IMAGE_TYPES:
        raise ValueError(f"Файл маскируется под изображение. Реальный тип: {actual_mime}")

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
    if all(c.isalnum() for c in v):
        raise ValueError("Пароль должен содержать хотя бы один спецсимвол")
    return v
