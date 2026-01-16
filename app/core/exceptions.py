class UserNotFoundError(Exception):
    def __init__(self, *, user_id: int | None = None, email: str | None = None) -> None:
        if user_id is None and email is None:
            raise ValueError("UserNotFoundError requires user_id or email")

        self.user_id = user_id
        self.email = email

        if user_id is not None:
            msg = f"User with id={user_id} not found"
        else:
            msg = f"User with email={email} not found"

        super().__init__(msg)


class UserAlreadyExistsError(Exception):
    def __init__(self, email: str) -> None:
        self.email = email
        super().__init__(f"User with email={email} already exists")
