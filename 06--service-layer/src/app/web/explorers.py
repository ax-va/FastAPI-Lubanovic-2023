from fastapi import APIRouter

from app.models.explorer import Explorer
from app.services import explorers

service = explorers
router = APIRouter(prefix="/explorers")


@router.get("")
@router.get("/")
def get_all() -> list[Explorer]:
    return service.get_all()


@router.get("/{explorer_id}")
@router.get("/{explorer_id}/")
def get_one(explorer_id: int) -> Explorer | None:
    return service.get_one(explorer_id)


@router.post("")
@router.post("/")
def create(explorer: Explorer) -> Explorer:
    return service.create(explorer)


@router.put("/{explorer_id}")
@router.put("/{explorer_id}/")
def replace(explorer_id: int, explorer: Explorer) -> Explorer | None:
    return service.replace(explorer_id, explorer)


@router.patch("/{explorer_id}")
@router.patch("/{explorer_id}/")
def modify(explorer_id: int) -> Explorer:
    raise NotImplementedError()


@router.delete("/{explorer_id}")
@router.delete("/{explorer_id}/")
def delete(explorer_id: int) -> bool:
    return service.delete(explorer_id)
