from fastapi import APIRouter, Depends

from app.models.explorers import ExplorerRequest, ExplorerResponse
from app.services import explorers
from app.services.errors import NotFoundError
from app.web.errors import resource_with_id_not_found

service = explorers
router = APIRouter(prefix="/explorers", tags=["Explorers"])


@router.get("")
def get_all() -> list[ExplorerResponse]:
    return service.get_all()


@router.get("/{explorer_id}")
def get_by_id(explorer_id: int) -> ExplorerResponse:
    explorer = service.get_by_id(explorer_id)

    if explorer is None:
        raise resource_with_id_not_found(f"Explorer with ID {explorer_id} not found")

    return explorer


@router.post("", status_code=201)  # 201 Created
def create(explorer: ExplorerRequest) -> ExplorerResponse:
    return service.create(explorer)


@router.put("/{explorer_id}")
def replace(explorer_id: int, explorer: ExplorerRequest) -> ExplorerResponse:
    try:
        explorer = service.replace(explorer_id, explorer)

    except NotFoundError as e:
        raise resource_with_id_not_found(str(e))

    return explorer


@router.patch("/{explorer_id}")
def modify(explorer_id: int) -> ExplorerResponse | None:
    raise NotImplementedError()


@router.delete("/{explorer_id}")
def delete(explorer_id: int) -> None:
    try:
        service.delete(explorer_id)

    except NotFoundError as e:
        raise resource_with_id_not_found(str(e))
