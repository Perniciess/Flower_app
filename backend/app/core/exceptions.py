from fastapi import HTTPException


class UserNotFoundError(HTTPException):
    def __init__(
        self, *, user_id: int | None = None, phone_number: str | None = None
    ) -> None:
        if user_id is not None:
            detail = f"Пользователь с ID={user_id} не найден"
        else:
            detail = f"Пользователь с номером={phone_number} не найден"
        super().__init__(status_code=404, detail=detail)


class UserAlreadyExistsError(HTTPException):
    def __init__(self, phone_number: str) -> None:
        super().__init__(
            status_code=409,
            detail=f"Пользователь с таким phone_number={phone_number} уже существует",
        )


class UserNotUpdatedError(HTTPException):
    def __init__(self, user_id: int, message: str | None = None) -> None:
        super().__init__(
            status_code=400,
            detail=message
            or f"Не удалось обновить данные пользователя с user_id={user_id}",
        )


class PasswordsDoNotMatchError(HTTPException):
    def __init__(self, message: str | None = None) -> None:
        super().__init__(status_code=400, detail=message or "Неправильный пароль")


class InsufficientPermissionError(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=403, detail="Отсутствуют права на выполнение операции"
        )


class InvalidTokenError(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=403, detail="Невалидный токен")


class ProductNotFoundError(HTTPException):
    def __init__(self, product_id: int) -> None:
        super().__init__(status_code=404, detail=f"Товар с ID={product_id} не найден")


class ImageNotFoundError(HTTPException):
    def __init__(self, image_id: int) -> None:
        super().__init__(
            status_code=404, detail=f"Изображение с ID={image_id} не найдено"
        )


class CartAlreadyExistsError(HTTPException):
    def __init__(self, cart_id: int) -> None:
        super().__init__(
            status_code=409, detail=f"Корзина с ID={cart_id} уже существует"
        )


class CartNotFoundError(HTTPException):
    def __init__(self, cart_id: int | None = None, user_id: int | None = None) -> None:
        if user_id is not None:
            detail = f"Корзина пользователя c ID={user_id} не найдена"
        else:
            detail = f"Корзина с ID={cart_id} не найдена"
        super().__init__(status_code=404, detail=detail)


class CartItemNotFoundError(HTTPException):
    def __init__(self, cart_item_id: int) -> None:
        super().__init__(
            status_code=404, detail=f"Товар корзины с ID={cart_item_id} не найден"
        )


class UserCartMissingError(HTTPException):
    def __init__(self, user_id: int) -> None:
        super().__init__(
            status_code=404, detail=f"У пользователя с ID={user_id} нет корзины"
        )


class OrderNotFoundError(HTTPException):
    def __init__(self, order_id: int) -> None:
        super().__init__(status_code=404, detail=f"Заказ с ID={order_id} не найден")


class OrderNotUpdatedError(HTTPException):
    def __init__(self, order_id: int) -> None:
        super().__init__(
            status_code=404, detail=f"Не удалось изменить статус заказа с ID={order_id}"
        )


class EmptyCartError(HTTPException):
    def __init__(self, cart_id: int) -> None:
        super().__init__(status_code=404, detail=f"Корзина с ID={cart_id} пустая")


class PaymentCreationError(HTTPException):
    def __init__(self, order_id: int) -> None:
        super().__init__(
            status_code=502,
            detail=f"Ошибка создания платежа для заказа с ID={order_id}",
        )


class CategoryAlreadyExistsError(HTTPException):
    def __init__(self, slug: str) -> None:
        super().__init__(
            status_code=409,
            detail=f"Категория с таким slug={slug} уже существует",
        )


class CategoryParentNotFoundError(HTTPException):
    def __init__(self, parent_id: int) -> None:
        super().__init__(
            status_code=409,
            detail=f"Родительская категория с ID={parent_id} не найдена",
        )


class CategoryNotExistsError(HTTPException):
    def __init__(self, slug: str | None = None, category_id: int | None = None) -> None:
        if category_id is not None:
            detail = f"Категория с ID={category_id} не найдена"
        else:
            detail = f"Категория с slug={slug} не найдена"
        super().__init__(status_code=404, detail=detail)
