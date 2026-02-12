def validate_link_scheme(v: str | None) -> str | None:
    """Validate that link is HTTP or HTTPS URL."""
    if v is None or v == "":
        return None
    if not v.startswith(("http://", "https://")):
        raise ValueError("Link must be an HTTP or HTTPS URL")
    return v
