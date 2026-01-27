from pydantic_extra_types.phone_numbers import PhoneNumber


def normalize_phone(v: PhoneNumber) -> str:
    s = str(v)
    if s.startswith("tel:"):
        s = s[4:]
    return s.replace(" ", "").replace("-", "")


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
