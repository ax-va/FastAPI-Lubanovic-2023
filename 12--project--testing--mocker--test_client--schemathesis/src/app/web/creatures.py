from fastapi import APIRouter, HTTPException, Depends

from app.models.creatures import CreatureRequest, CreatureResponse
from app.models.users import UserResponse
from app.services import creatures
from app.services.errors import NotFoundError
from app.web.deps.auth import get_current_user, CurrentUser
from app.web.deps.database import DatabaseConnection
from app.web.errors import resource_with_id_not_found
from app.web.metadata import NOT_FOUND, UNAUTHORIZED

service = creatures
router = APIRouter(prefix="/creatures", tags=["Creatures"])


# public API
@router.get("")
def get_all(
    connection: DatabaseConnection,
) -> list[CreatureResponse]:
    return service.get_all(connection)


# public API
@router.get(
    "/{creature_id}",
    responses=NOT_FOUND,
)
def get_by_id(
    connection: DatabaseConnection,
    creature_id: int,
) -> CreatureResponse:
    creature = service.get_by_id(connection, creature_id)

    if creature is None:
        raise resource_with_id_not_found(f"Creature with ID {creature_id} not found")

    return creature


# API for only authenticated users
@router.post(
    "",
    status_code=201,  # 201 Created
    responses=UNAUTHORIZED,
)
def create(
    connection: DatabaseConnection,
    creature: CreatureRequest,
    _: CurrentUser,
) -> CreatureResponse:
    return service.create(connection, creature)


# API for only authenticated users
@router.put(
    "/{creature_id}",
    responses=UNAUTHORIZED | NOT_FOUND,
)
def replace(
    connection: DatabaseConnection,
    creature_id: int,
    creature: CreatureRequest,
    _: CurrentUser,
) -> CreatureResponse:
    try:
        creature = service.replace(connection, creature_id, creature)

    except NotFoundError as e:
        raise resource_with_id_not_found(str(e)) from e

    return creature


@router.patch("/{creature_id}")
def modify(creature_id: int) -> CreatureResponse | None:
    raise NotImplementedError()


# API for only authenticated users
@router.delete(
    "/{creature_id}",
    responses=UNAUTHORIZED | NOT_FOUND,
)
def delete(
    connection: DatabaseConnection,
    creature_id: int,
    _: CurrentUser,
) -> None:
    try:
        service.delete(connection, creature_id)

    except NotFoundError as e:
        raise resource_with_id_not_found(str(e)) from e
