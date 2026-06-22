class AppError(Exception):
    def __init__(self, message: str = "Application error") -> None:
        self.message = message
        super().__init__(message)


class ConflictError(AppError):
    def __init__(self, message: str = "Conflict") -> None:
        super().__init__(message)


class UnauthorizedError(AppError):
    def __init__(self, message: str = "Unauthorized") -> None:
        super().__init__(message)


class ForbiddenError(AppError):
    def __init__(self, message: str = "Forbidden") -> None:
        super().__init__(message)


class NotFoundError(AppError):
    def __init__(self, message: str = "Not found") -> None:
        super().__init__(message)


class ExternalServiceError(AppError):
    def __init__(self, message: str = "External service error") -> None:
        super().__init__(message)
