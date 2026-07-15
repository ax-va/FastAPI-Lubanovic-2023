from fastapi import HTTPException
from starlette import status


def resource_with_id_not_found(resource: str, resource_id: int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{resource} with id {resource_id} not found",
    )