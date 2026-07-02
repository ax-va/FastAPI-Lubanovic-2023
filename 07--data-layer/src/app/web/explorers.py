from fastapi import APIRouter

from app.models.explorer import Explorer
from app.services import explorers

service = explorers
router = APIRouter(prefix="/explorers")


@router.get("")
def get_all() -> list[Explorer]:
    return service.get_all()


@router.get("/{explorer_id}")
def get_one(explorer_id: int) -> Explorer | None:
    return service.get_one(explorer_id)


# all the remaining endpoints do nothing yet
@router.post("")
def create(explorer: Explorer) -> Explorer:
    return service.create(explorer)


@router.put("")
def replace(explorer_id: int, explorer: Explorer) -> Explorer | None:
    return service.replace(explorer_id, explorer)


@router.patch("")
def modify(explorer_id: int) -> Explorer | None:
    raise NotImplementedError()


@router.delete("/{explorer_id}")
def delete(explorer_id: int) -> bool:
    return service.delete(explorer_id)
