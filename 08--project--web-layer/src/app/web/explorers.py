from fastapi import APIRouter

from app.models.schemas.explorers import ExplorerRequest, ExplorerResponse
from app.services import explorers as explorers_service
from app.services.errors import NotFoundError
from app.web.deps.database import DatabaseConnection
from app.web.errors import resource_with_id_not_found

service = explorers_service
router = APIRouter(prefix="/explorers", tags=["Explorers"])


@router.get("")
def get_all(
    db_connection: DatabaseConnection,
) -> list[ExplorerResponse]:
    return service.get_all(db_connection)


@router.get("/{explorer_id}")
def get_by_id(
    db_connection: DatabaseConnection,
    explorer_id: int,
) -> ExplorerResponse:
    explorer_response: ExplorerResponse | None = service.get_by_id(db_connection, explorer_id)

    if explorer_response is None:
        raise resource_with_id_not_found(f"Explorer with ID {explorer_id} not found")

    return explorer_response


@router.post("", status_code=201)  # 201 Created
def create(
    db_connection: DatabaseConnection,
    explorer_request: ExplorerRequest,
) -> ExplorerResponse:
    return service.create(db_connection, explorer_request)


@router.put("/{explorer_id}")
def replace(
    db_connection: DatabaseConnection,
    explorer_id: int,
    explorer_request: ExplorerRequest,
) -> ExplorerResponse:
    try:
        explorer_response: ExplorerResponse = service.replace(db_connection, explorer_id, explorer_request)

    except NotFoundError as e:
        raise resource_with_id_not_found(str(e)) from e

    return explorer_response


@router.patch("/{explorer_id}")
def modify(explorer_id: int) -> ExplorerResponse | None:
    raise NotImplementedError()


@router.delete("/{explorer_id}")
def delete(
    db_connection: DatabaseConnection,
    explorer_id: int,
) -> None:
    try:
        service.delete(db_connection, explorer_id)

    except NotFoundError as e:
        raise resource_with_id_not_found(str(e)) from e
