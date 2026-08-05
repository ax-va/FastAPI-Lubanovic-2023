from fastapi import HTTPException
from starlette import status


def not_found(message: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=message,
    )