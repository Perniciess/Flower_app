class UserNotFoundError(Exception):
    def __init__(self, *, user_id: int | None = None, email: str | None = None) -> None:
        if user_id is None and email is None:
            raise ValueError("UserNotFoundError requires user_id or email")

        self.user_id = user_id
        self.email = email

        if user_id is not None:
            msg = f"Пользователь с ID={user_id} не найден"
        else:
            msg = f"Пользователь с email={email} не найден"

        super().__init__(msg)


class UserAlreadyExistsError(Exception):
    def __init__(self, email: str) -> None:
        self.email = email
        super().__init__(f"Пользователь с таким email={email} уже существует")


class PasswordsDoNotMatchError(Exception):
    def __init__(self) -> None:
        super().__init__("Неправильный пароль")


class InsufficientPermission(Exception):
    def __init__(self) -> None:
        super().__init__("Отсутствуют права на выполнение операции")


class InvalidToken(Exception):
    def __init__(self) -> None:
        super().__init__("Невалидный токен")


class FlowerNotFoundError(Exception):
    def __init__(self, flower_id: int) -> None:
        super().__init__(f"Цветок с ID={flower_id} не найден")


class ImageNotFoundError(Exception):
    def __init__(self, image_id: int) -> None:
        super().__init__(f"Изображение с ID={image_id} не найдено")


class CartAlreadyExistsException(Exception):
    def __init__(self, cart_id: int) -> None:
        super().__init__(f"Корзина с ID={cart_id} уже существует")


class CartNotFoundError(Exception):
    def __init__(self, cart_id: int) -> None:
        super().__init__(f"Корзина с ID={cart_id} не найдена")


class CartItemNotFoundError(Exception):
    def __init__(self, cart_item_id: int) -> None:
        super().__init__(f"Товар корзины с ID={cart_item_id} не найдена")
