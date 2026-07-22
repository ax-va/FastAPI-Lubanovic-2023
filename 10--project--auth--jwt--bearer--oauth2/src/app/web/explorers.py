from fastapi import APIRouter
from app.models.explorers import ExplorerRequest, ExplorerResponse
from app.services import explorers
from app.services.errors import NotFoundError
from app.web.deps.auth import CurrentUser
from app.web.deps.database import DatabaseConnection
from app.web.errors import resource_with_id_not_found

service = explorers
router = APIRouter(prefix="/explorers", tags=["Explorers"])


# public
@router.get("")
def get_all(
    connection: DatabaseConnection,
) -> list[ExplorerResponse]:
    return service.get_all(connection)


# public
@router.get("/{explorer_id}")
def get_by_id(
    connection: DatabaseConnection,
    explorer_id: int,
) -> ExplorerResponse:
    explorer = service.get_by_id(connection, explorer_id)

    if explorer is None:
        raise resource_with_id_not_found(f"Explorer with ID {explorer_id} not found")

    return explorer


@router.post("", status_code=201)  # 201 Created
def create(
    connection: DatabaseConnection,
    explorer: ExplorerRequest,
    _: CurrentUser,  # for authenticated users
) -> ExplorerResponse:
    return service.create(connection, explorer)


@router.put("/{explorer_id}")
def replace(
    connection: DatabaseConnection,
    explorer_id: int,
    explorer: ExplorerRequest,
    _: CurrentUser,  # for authenticated users
) -> ExplorerResponse:
    try:
        explorer = service.replace(connection, explorer_id, explorer)

    except NotFoundError as e:
        raise resource_with_id_not_found(str(e))

    return explorer


@router.patch("/{explorer_id}")
def modify(explorer_id: int) -> ExplorerResponse | None:
    raise NotImplementedError()


@router.delete("/{explorer_id}")
def delete(
    connection: DatabaseConnection,
    explorer_id: int,
    _: CurrentUser,  # for authenticated users
) -> None:
    try:
        service.delete(connection, explorer_id)

    except NotFoundError as e:
        raise resource_with_id_not_found(str(e))
