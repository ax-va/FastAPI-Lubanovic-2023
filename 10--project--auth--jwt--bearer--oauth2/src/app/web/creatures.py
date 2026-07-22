from fastapi import APIRouter

from app.models.creatures import CreatureRequest, CreatureResponse
from app.services import creatures
from app.services.errors import NotFoundError
from app.web.deps.auth import CurrentUser
from app.web.deps.database import DatabaseConnection
from app.web.errors import resource_with_id_not_found

service = creatures
router = APIRouter(prefix="/creatures", tags=["Creatures"])


# public
@router.get("")
def get_all(
    connection: DatabaseConnection,
) -> list[CreatureResponse]:
    return service.get_all(connection)

# public
@router.get("/{creature_id}")
def get_by_id(
    connection: DatabaseConnection,
    creature_id: int,
) -> CreatureResponse:
    creature = service.get_by_id(connection, creature_id)

    if creature is None:
        raise resource_with_id_not_found(f"Creature with ID {creature_id} not found")

    return creature


@router.post("", status_code=201)  # 201 Created
def create(
    connection: DatabaseConnection,
    creature: CreatureRequest,
    _: CurrentUser,  # for authenticated users
) -> CreatureResponse:
    return service.create(connection, creature)


@router.put("/{creature_id}")
def replace(
    connection: DatabaseConnection,
    creature_id: int,
    creature: CreatureRequest,
    _: CurrentUser,  # for authenticated users
) -> CreatureResponse:
    try:
        creature = service.replace(connection, creature_id, creature)

    except NotFoundError as e:
        raise resource_with_id_not_found(str(e)) from e

    return creature


@router.patch("/{creature_id}")
def modify(creature_id: int) -> CreatureResponse | None:
    raise NotImplementedError()


@router.delete("/{creature_id}")
def delete(
    connection: DatabaseConnection,
    creature_id: int,
    _: CurrentUser,  # for authenticated users
) -> None:
    try:
        service.delete(connection, creature_id)

    except NotFoundError as e:
        raise resource_with_id_not_found(str(e)) from e
