from fastapi import APIRouter

from app.models.schemas.creatures import CreatureRequest, CreatureResponse
from app.services import creatures as creatures_service
from app.services.errors import NotFoundError
from app.web.deps.auth import CurrentUser
from app.web.deps.database import DatabaseConnection
from app.web.errors import not_found

service = creatures_service
router = APIRouter(prefix="/creatures", tags=["Creatures"])


# public API
@router.get("")
def get_all(
    db_connection: DatabaseConnection,
) -> list[CreatureResponse]:
    return service.get_all(db_connection)


# public API
@router.get("/{creature_id}")
def get_by_id(
    db_connection: DatabaseConnection,
    creature_id: int,
) -> CreatureResponse:
    creature_response: CreatureResponse | None = service.get_by_id(db_connection, creature_id)

    if creature_response is None:
        raise not_found(f"Creature with ID {creature_id} not found")

    return creature_response


# API for only authenticated users
@router.post("", status_code=201)  # 201 Created
def create(
    db_connection: DatabaseConnection,
    creature: CreatureRequest,
    _: CurrentUser,
) -> CreatureResponse:
    return service.create(db_connection, creature)


# API for only authenticated users
@router.put("/{creature_id}")
def replace(
    db_connection: DatabaseConnection,
    creature_id: int,
    creature: CreatureRequest,
    _: CurrentUser,
) -> CreatureResponse:
    try:
        creature_response: CreatureResponse = service.replace(db_connection, creature_id, creature)

    except NotFoundError as e:
        raise not_found(str(e)) from e

    return creature_response


@router.patch("/{creature_id}")
def modify(creature_id: int) -> CreatureResponse | None:
    raise NotImplementedError()


# API for only authenticated users
@router.delete("/{creature_id}")
def delete(
    db_connection: DatabaseConnection,
    creature_id: int,
    _: CurrentUser,
) -> None:
    try:
        service.delete(db_connection, creature_id)

    except NotFoundError as e:
        raise not_found(str(e)) from e
