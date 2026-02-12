from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field

from app.models.products_model import Product, ProductType, bouquet_composition

if TYPE_CHECKING:
    from sqlalchemy import Select
    from sqlalchemy.orm import Query


class ProductFilter(Filter):
    flower_id: int | None = None
    name__ilike: str | None = None
    color__in: list[str] | None = None
    price__gte: Decimal | None = None
    price__lte: Decimal | None = None
    is_active: bool | None = None
    in_stock: bool | None = None
    search: str | None = None
    order_by: list[str] | None = Field(default=["sort_order"])
    type: ProductType | None = None

    def filter(self, query: Query | Select) -> Query | Select:  # type: ignore[override]
        """Apply filters to query, handling flower_id with JOIN."""
        if self.flower_id is not None:
            query = query.join(
                bouquet_composition,
                Product.id == bouquet_composition.c.product_id,
            ).where(bouquet_composition.c.flower_id == self.flower_id)

        # Temporarily nullify flower_id so super().filter() doesn't try to use it
        saved_flower_id = self.flower_id
        self.flower_id = None
        query = super().filter(query)
        self.flower_id = saved_flower_id
        return query

    class Constants(Filter.Constants):
        model = Product
        search_model_fields = ["name", "description"]  # noqa: RUF012
