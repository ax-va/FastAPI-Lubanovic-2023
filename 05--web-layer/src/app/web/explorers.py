from fastapi import APIRouter

from app.fake import explorer_repository
from app.models.explorer import Explorer

router = APIRouter(prefix="/explorers")


@router.get("")
def get_all() -> list[Explorer]:
    return explorer_repository.get_all()


@router.get("/{explorer_id}")
def get_one(explorer_id: int) -> Explorer | None:
    return explorer_repository.get_one(explorer_id)


# all the remaining endpoints do nothing yet
@router.post("")
def create(explorer: Explorer) -> Explorer:
    return explorer_repository.create(explorer)


@router.put("")
def replace(explorer: Explorer) -> Explorer:
    return explorer_repository.replace(explorer)


@router.patch("")
def modify(explorer: Explorer) -> Explorer:
    return explorer_repository.modify(explorer)


@router.delete("/{explorer_id}")
def delete(explorer_id: int) -> bool:
    return explorer_repository.delete(explorer_id)
