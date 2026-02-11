from fastapi import HTTPException


class UserNotFoundError(HTTPException):
    def __init__(self, *, user_id: int | None = None, phone_number: str | None = None) -> None:
        detail = "Пользователь не найден"
        super().__init__(status_code=404, detail=detail)


class UserAlreadyExistsError(HTTPException):
    def __init__(self, phone_number: str) -> None:
        super().__init__(
            status_code=409,
            detail="Пользователь с таким номером уже существует",
        )


class UserNotUpdatedError(HTTPException):
    def __init__(self, user_id: int, message: str | None = None) -> None:
        super().__init__(
            status_code=400,
            detail=message or "Не удалось обновить данные пользователя",
        )


class InvalidCredentialsError(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=401, detail="Неверный номер телефона или пароль")


class PasswordsDoNotMatchError(HTTPException):
    def __init__(self, message: str | None = None) -> None:
        super().__init__(status_code=400, detail=message or "Неправильный пароль")


class AccountLockedError(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=429,
            detail="Аккаунт временно заблокирован. Попробуйте через 15 минут",
        )


class InsufficientPermissionError(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=403, detail="Отсутствуют права на выполнение операции")


class InvalidTokenError(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=401, detail="Невалидный токен")


class ProductNotFoundError(HTTPException):
    def __init__(self, product_id: int) -> None:
        super().__init__(status_code=404, detail=f"Товар с ID={product_id} не найден")


class ImageNotFoundError(HTTPException):
    def __init__(self, image_id: int) -> None:
        super().__init__(status_code=404, detail=f"Изображение с ID={image_id} не найдено")


class CartAlreadyExistsError(HTTPException):
    def __init__(self, cart_id: int) -> None:
        super().__init__(status_code=409, detail=f"Корзина с ID={cart_id} уже существует")


class CartNotFoundError(HTTPException):
    def __init__(self, cart_id: int | None = None, user_id: int | None = None) -> None:
        detail = "Корзина не найдена"
        super().__init__(status_code=404, detail=detail)


class CartItemNotFoundError(HTTPException):
    def __init__(self, cart_item_id: int) -> None:
        super().__init__(status_code=404, detail=f"Товар корзины с ID={cart_item_id} не найден")


class UserCartMissingError(HTTPException):
    def __init__(self, user_id: int) -> None:
        super().__init__(status_code=404, detail="У пользователя нет корзины")


class CategoryAlreadyExistsError(HTTPException):
    def __init__(self, slug: str) -> None:
        super().__init__(
            status_code=409,
            detail=f"Категория с таким slug={slug} уже существует",
        )


class CategoryParentNotFoundError(HTTPException):
    def __init__(self, parent_id: int) -> None:
        super().__init__(
            status_code=404,
            detail=f"Родительская категория с ID={parent_id} не найдена",
        )


class CategoryNotExistsError(HTTPException):
    def __init__(self, slug: str | None = None, category_id: int | None = None) -> None:
        if category_id is not None:
            detail = f"Категория с ID={category_id} не найдена"
        else:
            detail = f"Категория с slug={slug} не найдена"
        super().__init__(status_code=404, detail=detail)


class CategoryCycleError(HTTPException):
    def __init__(self, category_id: int, parent_id: int) -> None:
        super().__init__(
            status_code=409,
            detail=f"Циклическая зависимость: категория {category_id} не может быть дочерней для {parent_id}",
        )


class DiscountNotFoundError(HTTPException):
    def __init__(self, discount_id: int) -> None:
        super().__init__(status_code=404, detail=f"Скидка с ID={discount_id} не найдена")


class FavouriteItemAlreadyExistsError(HTTPException):
    def __init__(self, product_id: int) -> None:
        super().__init__(status_code=409, detail=f"Товар с ID={product_id} уже есть в понравившихся")


class FavouriteItemNotFoundError(HTTPException):
    def __init__(self, product_id: int) -> None:
        super().__init__(status_code=404, detail=f"Товар с ID={product_id} не найден в понравившихся")


class PickupPointNotFoundError(HTTPException):
    def __init__(self, pickup_point_id: int) -> None:
        super().__init__(
            status_code=404,
            detail=f"Точка самовывоза с ID={pickup_point_id} не найдена",
        )


class PickupPointNotActiveError(HTTPException):
    def __init__(self, pickup_point_id: int) -> None:
        super().__init__(status_code=400, detail=f"Точка самовывоза с ID={pickup_point_id} неактивна")


class FlowerNotFoundError(HTTPException):
    def __init__(self, flower_id: int) -> None:
        super().__init__(status_code=404, detail=f"Цветок с ID={flower_id} не найден")


class BannerNotFoundError(HTTPException):
    def __init__(self, banner_id: int) -> None:
        super().__init__(status_code=404, detail=f"Баннер с ID={banner_id} не найден")


class EmptyCartError(HTTPException):
    def __init__(self, cart_id: int) -> None:
        super().__init__(status_code=400, detail=f"Корзина с ID={cart_id} пустая")


class ProductOutOfStockError(HTTPException):
    def __init__(self, product_ids: list[int]) -> None:
        ids_str = ", ".join(str(pid) for pid in product_ids)
        super().__init__(status_code=400, detail=f"Товары не в наличии: {ids_str}")


class OrderNotFoundError(HTTPException):
    def __init__(self, order_id: int) -> None:
        super().__init__(status_code=404, detail=f"Заказ с ID={order_id} не найден")


class OrderNotUpdatedError(HTTPException):
    def __init__(self, order_id: int) -> None:
        super().__init__(status_code=409, detail=f"Не удалось изменить статус заказа с ID={order_id}")


class PaymentCreationError(HTTPException):
    def __init__(self, order_id: int) -> None:
        super().__init__(
            status_code=502,
            detail=f"Ошибка создания платежа для заказа с ID={order_id}",
        )
