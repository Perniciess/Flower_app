from pydantic_extra_types.phone_numbers import PhoneNumber


def normalize_phone(v: PhoneNumber) -> str:
    s = str(v)
    if s.startswith("tel:"):
        s = s[4:]
    return s.replace(" ", "").replace("-", "")
