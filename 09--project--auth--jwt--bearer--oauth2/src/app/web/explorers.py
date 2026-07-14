from fastapi import APIRouter, HTTPException, Depends

from app.models.explorers import ExplorerRequest, ExplorerResponse
from app.models.users import UserResponse
from app.repositories.errors import NotFoundError
from app.services import explorers
from app.web.deps.auth import get_current_user

service = explorers
router = APIRouter(prefix="/explorers", tags=["Explorers"])


# public API
@router.get("")
def get_all() -> list[ExplorerResponse]:
    return service.get_all()


# public API
@router.get("/{explorer_id}")
def get_by_id(explorer_id: int) -> ExplorerResponse:
    explorer = service.get_by_id(explorer_id)
    if explorer is None:
        raise HTTPException(
            status_code=404,
            detail=f"Explorer with ID {explorer_id} not found",
        )

    return explorer


# API for only authenticated users
@router.post("", status_code=201)  # 201 Created
def create(
    explorer: ExplorerRequest,
    _: UserResponse = Depends(get_current_user),
) -> ExplorerResponse:
    return service.create(explorer)


# API for only authenticated users
@router.put("/{explorer_id}")
def replace(
    explorer_id: int,
    explorer: ExplorerRequest,
    _: UserResponse = Depends(get_current_user),
) -> ExplorerResponse:
    try:
        explorer = service.replace(explorer_id, explorer)

    except NotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    return explorer


@router.patch("/{explorer_id}")
def modify(explorer_id: int) -> ExplorerResponse | None:
    raise NotImplementedError()


# API for only authenticated users
@router.delete("/{explorer_id}")
def delete(
    explorer_id: int,
    _: UserResponse = Depends(get_current_user),
) -> bool:
    deleted = service.delete(explorer_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Explorer with ID {explorer_id} not found",
        )

    return deleted
