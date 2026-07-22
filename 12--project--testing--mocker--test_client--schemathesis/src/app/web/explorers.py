from fastapi import APIRouter, HTTPException, Depends

from app.models.explorers import ExplorerRequest, ExplorerResponse
from app.models.users import UserResponse
from app.services import explorers
from app.services.errors import NotFoundError
from app.web.deps.auth import get_current_user, CurrentUser
from app.web.deps.database import DatabaseConnection
from app.web.errors import resource_with_id_not_found
from app.web.metadata import NOT_FOUND, UNAUTHORIZED

service = explorers
router = APIRouter(prefix="/explorers", tags=["Explorers"])


# public API
@router.get("")
def get_all(
    connection: DatabaseConnection,
) -> list[ExplorerResponse]:
    return service.get_all(connection)


# public API
@router.get(
    "/{explorer_id}",
    responses=NOT_FOUND,
)
def get_by_id(
    connection: DatabaseConnection,
    explorer_id: int,
) -> ExplorerResponse:
    explorer = service.get_by_id(connection, explorer_id)

    if explorer is None:
        raise resource_with_id_not_found(f"Explorer with ID {explorer_id} not found")

    return explorer


# API for only authenticated users
@router.post(
    "",
    status_code=201,  # 201 Created
    responses=UNAUTHORIZED,
)
def create(
    connection: DatabaseConnection,
    explorer: ExplorerRequest,
    _: CurrentUser,
) -> ExplorerResponse:
    return service.create(connection, explorer)


# API for only authenticated users
@router.put(
    "/{explorer_id}",
    responses=UNAUTHORIZED | NOT_FOUND,
)
def replace(
    connection: DatabaseConnection,
    explorer_id: int,
    explorer: ExplorerRequest,
    _: CurrentUser,
) -> ExplorerResponse:
    try:
        explorer = service.replace(connection, explorer_id, explorer)

    except NotFoundError as e:
        raise resource_with_id_not_found(str(e))

    return explorer


@router.patch("/{explorer_id}")
def modify(explorer_id: int) -> ExplorerResponse | None:
    raise NotImplementedError()


# API for only authenticated users
@router.delete(
    "/{explorer_id}",
    responses=UNAUTHORIZED | NOT_FOUND,
)
def delete(
    connection: DatabaseConnection,
    explorer_id: int,
    _: CurrentUser,
) -> None:
    try:
        service.delete(connection, explorer_id)

    except NotFoundError as e:
        raise resource_with_id_not_found(str(e))
