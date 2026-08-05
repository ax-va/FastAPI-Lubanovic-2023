from fastapi import APIRouter

from app.models.schemas.creatures import CreatureRequest, CreatureResponse
from app.services import creatures as creatures_service
from app.services.errors import NotFoundError
from app.web.deps.database import DatabaseConnection
from app.web.errors import not_found

service = creatures_service
router = APIRouter(prefix="/creatures", tags=["Creatures"])


@router.get("")
def get_all(
    db_connection: DatabaseConnection,
) -> list[CreatureResponse]:
    return service.get_all(db_connection)


@router.get("/{creature_id}")
def get_by_id(
    db_connection: DatabaseConnection,
    creature_id: int,
) -> CreatureResponse:
    creature_response: CreatureResponse | None = service.get_by_id(db_connection, creature_id)

    if creature_response is None:
        raise not_found(f"Creature with ID {creature_id} not found")

    return creature_response


@router.post("", status_code=201)  # 201 Created
def create(
    db_connection: DatabaseConnection,
    creature_request: CreatureRequest,
) -> CreatureResponse:
    return service.create(db_connection, creature_request)


@router.put("/{creature_id}")
def replace(
    db_connection: DatabaseConnection,
    creature_id: int,
    creature_request: CreatureRequest,
) -> CreatureResponse:
    try:
        creature_response: CreatureResponse = service.replace(db_connection, creature_id, creature_request)

    except NotFoundError as e:
        raise not_found(str(e)) from e

    return creature_response


@router.patch("/{creature_id}")
def modify(creature_id: int) -> CreatureResponse | None:
    raise NotImplementedError()


@router.delete("/{creature_id}")
def delete(
    db_connection: DatabaseConnection,
    creature_id: int,
) -> None:
    try:
        service.delete(db_connection, creature_id)

    except NotFoundError as e:
        raise not_found(str(e)) from e
