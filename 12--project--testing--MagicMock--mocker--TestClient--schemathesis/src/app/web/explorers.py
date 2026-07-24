from fastapi import APIRouter

from app.models.schemas.explorers import ExplorerRequest, ExplorerResponse
from app.services import explorers
from app.services.errors import NotFoundError
from app.web.deps.auth import CurrentUser
from app.web.deps.database import DatabaseConnection
from app.web.errors import resource_with_id_not_found
from app.web.metadata import NOT_FOUND, UNAUTHORIZED

service = explorers
router = APIRouter(prefix="/explorers", tags=["Explorers"])


# public API
@router.get("")
def get_all(
    db_connection: DatabaseConnection,
) -> list[ExplorerResponse]:
    return service.get_all(db_connection)


# public API
@router.get(
    "/{explorer_id}",
    responses=NOT_FOUND,
)
def get_by_id(
    db_connection: DatabaseConnection,
    explorer_id: int,
) -> ExplorerResponse:
    explorer_response = service.get_by_id(db_connection, explorer_id)

    if explorer_response is None:
        raise resource_with_id_not_found(f"Explorer with ID {explorer_id} not found")

    return explorer_response


# API for only authenticated users
@router.post(
    "",
    status_code=201,  # 201 Created
    responses=UNAUTHORIZED,
)
def create(
    db_connection: DatabaseConnection,
    explorer: ExplorerRequest,
    _: CurrentUser,
) -> ExplorerResponse:
    return service.create(db_connection, explorer)


# API for only authenticated users
@router.put(
    "/{explorer_id}",
    responses=UNAUTHORIZED | NOT_FOUND,
)
def replace(
    db_connection: DatabaseConnection,
    explorer_id: int,
    explorer: ExplorerRequest,
    _: CurrentUser,
) -> ExplorerResponse:
    try:
        explorer_response = service.replace(db_connection, explorer_id, explorer)

    except NotFoundError as e:
        raise resource_with_id_not_found(str(e))

    return explorer_response


@router.patch("/{explorer_id}")
def modify(explorer_id: int) -> ExplorerResponse | None:
    raise NotImplementedError()


# API for only authenticated users
@router.delete(
    "/{explorer_id}",
    responses=UNAUTHORIZED | NOT_FOUND,
)
def delete(
    db_connection: DatabaseConnection,
    explorer_id: int,
    _: CurrentUser,
) -> None:
    try:
        service.delete(db_connection, explorer_id)

    except NotFoundError as e:
        raise resource_with_id_not_found(str(e))
