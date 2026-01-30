from decimal import Decimal

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field

from .model import Flower


class FlowerFilter(Filter):
    name__ilike: str | None = None
    color__in: list[str] | None = None
    price__gte: Decimal | None = None
    price__lte: Decimal | None = None
    search: str | None = None
    order_by: list[str] | None = Field(default=["id"])

    class Constants(Filter.Constants):
        model = Flower
        search_model_fields = ["name", "description"]
