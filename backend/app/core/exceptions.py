class UserNotFoundError(Exception):
    def __init__(self, *, user_id: int | None = None, phone_number: str | None = None) -> None:
        if user_id is None and phone_number is None:
            raise ValueError("UserNotFoundError requires user_id or phone_number")

        self.user_id = user_id
        self.phone_number = phone_number

        if user_id is not None:
            msg = f"Пользователь с ID={user_id} не найден"
        else:
            msg = f"Пользователь с номером={phone_number} не найден"

        super().__init__(msg)


class UserAlreadyExistsError(Exception):
    def __init__(self, phone_number: str) -> None:
        self.phone_number = phone_number
        super().__init__(f"Пользователь с таким phone_number={phone_number} уже существует")


class PasswordsDoNotMatchError(Exception):
    def __init__(self) -> None:
        super().__init__("Неправильный пароль")


class InsufficientPermissionError(Exception):
    def __init__(self) -> None:
        super().__init__("Отсутствуют права на выполнение операции")


class InvalidTokenError(Exception):
    def __init__(self) -> None:
        super().__init__("Невалидный токен")


class FlowerNotFoundError(Exception):
    def __init__(self, flower_id: int) -> None:
        super().__init__(f"Цветок с ID={flower_id} не найден")


class ImageNotFoundError(Exception):
    def __init__(self, image_id: int) -> None:
        super().__init__(f"Изображение с ID={image_id} не найдено")


class CartAlreadyExistsError(Exception):
    def __init__(self, cart_id: int) -> None:
        super().__init__(f"Корзина с ID={cart_id} уже существует")


class CartNotFoundError(Exception):
    def __init__(self, cart_id: int) -> None:
        super().__init__(f"Корзина с ID={cart_id} не найдена")


class CartItemNotFoundError(Exception):
    def __init__(self, cart_item_id: int) -> None:
        super().__init__(f"Товар корзины с ID={cart_item_id} не найдена")
