import re


def validate_slug(v: str) -> str:
    v = v.lower().strip()

    if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", v):
        raise ValueError(
            "Slug может содержать только строчные латинские буквы, цифры и дефисы. "
            "Дефис не может быть в начале или конце."
        )

    return v
