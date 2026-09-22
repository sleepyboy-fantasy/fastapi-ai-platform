class AppException(Exception):

    def __init__(
        self,
        code: int,
        message: str
    ):
        self.code = code
        self.message = message


class UserAlreadyExistsException(AppException):

    def __init__(self):
        super().__init__(
            code=400,
            message="Username already exists"
        )


class EmailAlreadyExistsException(AppException):

    def __init__(self):
        super().__init__(
            code=400,
            message="Email already exists"
        )


class InvalidCredentialsException(AppException):

    def __init__(self):
        super().__init__(
            code=401,
            message="Invalid username or password"
        )
