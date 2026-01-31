# План: Система скидок на товары

## Что реализуем
Скидки на товары или категории через отдельный модуль `discounts`. Без сроков, лимитов, трекинга. Без комбинирования — применяется одна лучшая скидка.

**Два режима задания скидки:**
- **На товар**: админ задаёт либо новую цену (`new_price`), либо процент (`percentage`) — система вычисляет второе значение автоматически
- **На категорию**: только процент (`percentage`) — `new_price` вычисляется для каждого товара индивидуально

## Новый модуль: `backend/app/modules/discounts/`

### Модель (`model.py`)

**DiscountType** (StrEnum): `PRODUCT` | `CATEGORY`

**Discount:**
- `id` (PK)
- `name` — str, название
- `discount_type` — DiscountType
- `percentage` — Decimal(5,2), nullable — процент скидки (0-100)
- `new_price` — Decimal(10,2), nullable — новая цена (только для PRODUCT)
- `is_active` — bool, default=True
- `product_id` — FK → Product, nullable (для типа PRODUCT)
- `category_id` — FK → Category, nullable (для типа CATEGORY)
- `created_at`, `updated_at`

**Constraint:** ровно одно из `product_id` / `category_id` заполнено (CheckConstraint).
**Constraint:** для CATEGORY `new_price` должно быть NULL.
**Constraint:** ровно одно из `percentage` / `new_price` заполнено.

### Схемы (`schema.py`)

**DiscountCreateProduct:**
- `name`, `product_id`
- `percentage: Decimal | None`, `new_price: Decimal | None` — одно из двух обязательно
- `is_active` (default=True)
- Валидатор: ровно одно из percentage/new_price

**DiscountCreateCategory:**
- `name`, `category_id`, `percentage`
- `is_active` (default=True)

**DiscountUpdate:** все поля optional

**DiscountResponse:**
- Все поля модели + вычисленные: если задан `new_price` → вычислить `percentage`, если задан `percentage` → `new_price` вычисляется per-product

**DiscountBrief** (для ProductResponse):
- `percentage`, `new_price`

### Репозиторий (`repository.py`)

- CRUD
- `get_active_for_product(product_id)` — скидки напрямую на товар
- `get_active_for_category_ids(category_ids)` — скидки на категории товара
- `get_active_for_products(product_ids)` — batch: все скидки для списка товаров (прямые + через категории)

### Сервис (`service.py`)

- CRUD (admin)
- `create_product_discount(data)` — если задан `new_price`, вычисляет `percentage` = `(price - new_price) / price * 100`; если задан `percentage`, оставляет `new_price = None`
- `create_category_discount(data)` — только с `percentage`
- `get_best_discount_for_product(product)` — находит лучшую скидку (прямая на товар или через категорию), возвращает (discounted_price, discount_brief)
- `enrich_products(products)` — batch-обогащение списка товаров

### Роутер (`router.py`)

- `POST /discounts/product` — создать скидку на товар (admin)
- `POST /discounts/category` — создать скидку на категорию (admin)
- `GET /discounts` — список с пагинацией (admin)
- `GET /discounts/{id}` — детали (admin)
- `PATCH /discounts/{id}` — обновить (admin)
- `DELETE /discounts/{id}` — удалить (admin)

## Изменения в существующих модулях

### Products
- **`schema.py`**: в `ProductResponse` добавить `discount: DiscountBrief | None = None` и `discounted_price: Decimal | None = None`
- **`service.py`**: при `get_products()` и `get_product()` обогащать ответ через `discount_service.enrich_products()`

### Carts
- **`service.py`**: в `create_cart_item()` — запрашивать `discount_service.get_best_discount_for_product()` и записывать `discounted_price` в `CartItem.price` если скидка есть

### Orders
- **`service.py`**: в `create_order()` — пересчитать цены товаров в корзине с актуальными скидками перед отправкой в оплату
- **`model.py`**: добавить `discount_amount: Decimal(10,2)` (default=0) — общая сумма скидки в заказе

## Файлы

**Создать:**
- `backend/app/modules/discounts/__init__.py`
- `backend/app/modules/discounts/model.py`
- `backend/app/modules/discounts/schema.py`
- `backend/app/modules/discounts/repository.py`
- `backend/app/modules/discounts/service.py`
- `backend/app/modules/discounts/router.py`

**Изменить:**
- `backend/app/modules/products/schema.py`
- `backend/app/modules/products/service.py`
- `backend/app/modules/carts/service.py`
- `backend/app/modules/orders/service.py`
- `backend/app/modules/orders/model.py`
- `backend/app/main.py`

## Проверка

1. `alembic revision --autogenerate -m "add discounts"` + `alembic upgrade head`
2. `ruff check app/ && ruff format app/`
3. Создать скидку на товар (new_price=4000 при price=5000) → проверить что percentage=20 вычислился
4. Создать скидку на категорию (percentage=15) → все товары категории показывают discounted_price
5. `GET /products` → товары со скидками имеют discount и discounted_price
6. Добавить в корзину → CartItem.price = discounted_price
7. Оформить заказ → total учитывает скидку, discount_amount заполнен
