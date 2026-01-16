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
