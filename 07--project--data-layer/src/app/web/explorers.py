from fastapi import APIRouter, HTTPException

from app.models.explorers import ExplorerRequest, ExplorerResponse
from app.services import explorers

service = explorers
router = APIRouter(prefix="/explorers")


@router.get("")
@router.get("/")
def get_all() -> list[ExplorerResponse]:
    return service.get_all()


@router.get("/{explorer_id}")
@router.get("/{explorer_id}/")
def get_by_id(explorer_id: int) -> ExplorerResponse:
    explorer = service.get_by_id(explorer_id)
    if explorer is None:
        raise HTTPException(
            status_code=404,
            detail=f"Explorer with ID {explorer_id} not found",
        )
    return explorer


@router.post("")
@router.post("/")
def create(explorer: ExplorerRequest) -> ExplorerResponse:
    return service.create(explorer)


@router.put("/{explorer_id}")
@router.put("/{explorer_id}/")
def replace(explorer_id: int, explorer: ExplorerRequest) -> ExplorerResponse:
    explorer = service.replace(explorer_id, explorer)
    if explorer is None:
        raise HTTPException(
            status_code=404,
            detail=f"Explorer with ID {explorer_id} not found",
        )
    return explorer


@router.patch("/{explorer_id}")
@router.patch("/{explorer_id}/")
def modify(explorer_id: int) -> ExplorerResponse | None:
    raise NotImplementedError()


@router.delete("/{explorer_id}")
@router.delete("/{explorer_id}/")
def delete(explorer_id: int) -> bool:
    deleted = service.delete(explorer_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Explorer with ID {explorer_id} not found",
        )
    return deleted
