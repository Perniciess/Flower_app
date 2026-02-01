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
