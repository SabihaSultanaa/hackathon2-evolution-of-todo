"""Custom exceptions and exception handlers."""

from fastapi import HTTPException
from fastapi.responses import JSONResponse


class NotFoundError(HTTPException):
    """Resource not found error."""

    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=404, detail=detail)


class UnauthorizedError(HTTPException):
    """Unauthorized error."""

    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(status_code=401, detail=detail)


class ConflictError(HTTPException):
    """Conflict error."""

    def __init__(self, detail: str = "Resource already exists"):
        super().__init__(status_code=409, detail=detail)
