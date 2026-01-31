from collections.abc import Sequence
from decimal import Decimal

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import DiscountNotFoundError, ProductNotFoundError
from app.modules.products.model import Product

from . import repository as discount_repository
from .model import Discount, DiscountType
from .schema import DiscountCreate, DiscountResponse, DiscountUpdate


async def create_discount(*, session: AsyncSession, discount_data: DiscountCreate) -> DiscountResponse:
    """
    Создаёт акцию, если указан product_id то скидка на 1 товар, иначе скидка на категорию.

    Args:
        session: сессия базы данных
        discount_data: данные для создания акции

    Returns:
        DiscountResponse об акции

    Raises:
        ProductNotFoundError: если товар не найден по идентификатору при создании акции на 1 товар
    """
    discount_type = DiscountType.PRODUCT if discount_data.product_id else DiscountType.CATEGORY

    if discount_data.product_id and discount_data.new_price is not None:
        product = await session.get(Product, discount_data.product_id)
        if not product:
            raise ProductNotFoundError(product_id=discount_data.product_id)
        discount_data = discount_data.model_copy(
            update={"percentage": _calc_percentage(product.price, discount_data.new_price)}
        )

    data = discount_data.model_dump()
    data["discount_type"] = discount_type

    discount = await discount_repository.create_discount(session=session, discount_data=DiscountCreate(**data))
    return DiscountResponse.model_validate(discount)


async def get_discount(*, session: AsyncSession, discount_id: int) -> DiscountResponse:
    """
    Возвращает информацию об акции по идентификатору.

    Args:
        session: сессия базы данных
        discount_id: идентификатор акции

    Returns:
        DiscountResponse об акции

    Raises:
        DiscountNotFoundError: если акция не найдена
    """
    discount = await discount_repository.get_discount(session=session, discount_id=discount_id)
    if not discount:
        raise DiscountNotFoundError(discount_id=discount_id)
    return DiscountResponse.model_validate(discount)


async def get_discounts(*, session: AsyncSession) -> Page[DiscountResponse]:
    """
    Возвращает пагинированный список всех акций.

    Args:
        session: сессия базы данных

    Returns:
        Page[DiscountResponse] с пагинированным списком акций
    """
    query = discount_repository.get_discounts_query()
    return await paginate(session, query)


async def update_discount(
    *, session: AsyncSession, discount_id: int, discount_data: DiscountUpdate
) -> DiscountResponse:
    """
    Обновляет информацию о категории в базе данных.

    Args:
        session: сессия базы данных
        discount_id: идентификатор акции
        discount_data: новые данные акции

    Returns:
        DiscountResponse с данными обновленной акции

    Raises:
        DiscountNotFoundError: если акция не существует
    """
    existing = await discount_repository.get_discount(session=session, discount_id=discount_id)
    if not existing:
        raise DiscountNotFoundError(discount_id=discount_id)

    update_data = discount_data.model_dump(exclude_unset=True)

    if "new_price" in update_data and update_data["new_price"] is not None and existing.product_id:
        product = await session.get(Product, existing.product_id)
        if product:
            update_data["percentage"] = _calc_percentage(product.price, update_data["new_price"])

    discount = await discount_repository.update_discount(
        session=session, discount_id=discount_id, discount_data=DiscountUpdate(**update_data)
    )
    if not discount:
        raise DiscountNotFoundError(discount_id=discount_id)
    return DiscountResponse.model_validate(discount)


async def delete_discount(*, session: AsyncSession, discount_id: int) -> None:
    """
    Удаляет акцию.

    Args:
        session: сессия базы данных
        discount_id: идентификатор акции

    Returns:
        None

    Raises:
        DiscountNotFoundError: если акция не существует
    """
    existing = await discount_repository.get_discount(session=session, discount_id=discount_id)
    if not existing:
        raise DiscountNotFoundError(discount_id=discount_id)

    deleted = await discount_repository.delete_discount(session=session, discount_id=discount_id)
    if not deleted:
        raise DiscountNotFoundError(discount_id=discount_id)


async def enrich_products(
    *, session: AsyncSession, products: Sequence[Product]
) -> dict[int, tuple[Decimal | None, Discount | None]]:
    """
    Дополняет список товаров информацией о скидках.

    Для каждого товара ищет активную скидку: сначала персональную (на товар),
    затем по категории. Возвращает словарь с итоговой ценой и объектом скидки.

    Args:
        session: сессия базы данных
        products: список товаров для обогащения

    Returns:
        Словарь {product_id: (цена со скидкой, скидка)} — значения (None, None), если скидки нет.
    """
    if not products:
        return {}

    product_ids = [p.id for p in products]

    product_discounts = await discount_repository.get_active_for_products(session=session, product_ids=product_ids)

    product_discount_map: dict[int, Discount] = {}
    for d in product_discounts:
        if d.product_id is not None:
            product_discount_map[d.product_id] = d

    all_category_ids: set[int] = set()
    for p in products:
        if hasattr(p, "categories") and p.categories:
            for cat in p.categories:
                all_category_ids.add(cat.id)

    category_discounts = await discount_repository.get_active_for_category_ids(
        session=session, category_ids=list(all_category_ids)
    )

    category_discount_map: dict[int, Discount] = {}
    for d in category_discounts:
        if d.category_id is not None:
            category_discount_map[d.category_id] = d

    result: dict[int, tuple[Decimal | None, Discount | None]] = {}

    for p in products:
        discount = product_discount_map.get(p.id)

        if not discount and hasattr(p, "categories") and p.categories:
            for cat in p.categories:
                if cat.id in category_discount_map:
                    discount = category_discount_map[cat.id]
                    break

        if discount:
            result[p.id] = (_apply_discount(p.price, discount), discount)
        else:
            result[p.id] = (None, None)

    return result


def _calc_percentage(original_price: Decimal, new_price: Decimal) -> Decimal:
    """
    Вычисляет процент скидки по исходной и новой цене.

    Args:
        original_price: старая цена
        new_price: новая цена
    Returns:
        Decimal: % скидки
    """
    return ((original_price - new_price) / original_price * 100).quantize(Decimal("0.01"))


def _apply_discount(price: Decimal, discount: Discount) -> Decimal:
    """
    Применяет скидку к цене: возвращает new_price или рассчитывает цену по проценту.

    Args:
        price: старая цена
        discount: % скидки
    Returns:
        Decimal: новая цена
    """
    if discount.new_price is not None:
        return discount.new_price
    if discount.percentage is None:
        return price
    return (price * (100 - discount.percentage) / 100).quantize(Decimal("0.01"))
