from fastapi import APIRouter, Depends

from app.models.creatures import CreatureRequest, CreatureResponse
from app.services import creatures
from app.services.errors import NotFoundError
from app.web.errors import resource_with_id_not_found

service = creatures
router = APIRouter(prefix="/creatures", tags=["Creatures"])


@router.get("")
def get_all() -> list[CreatureResponse]:
    return service.get_all()


@router.get("/{creature_id}")
def get_by_id(creature_id: int) -> CreatureResponse:
    creature = service.get_by_id(creature_id)

    if creature is None:
        raise resource_with_id_not_found(f"Creature with ID {creature_id} not found")

    return creature


@router.post("", status_code=201)  # 201 Created
def create(creature: CreatureRequest) -> CreatureResponse:
    return service.create(creature)


@router.put("/{creature_id}")
def replace(creature_id: int, creature: CreatureRequest) -> CreatureResponse:
    try:
        creature = service.replace(creature_id, creature)

    except NotFoundError as e:
        raise resource_with_id_not_found(str(e))

    return creature


@router.patch("/{creature_id}")
def modify(creature_id: int) -> CreatureResponse | None:
    raise NotImplementedError()


@router.delete("/{creature_id}")
def delete(creature_id: int) -> None:
    try:
        service.delete(creature_id)

    except NotFoundError as e:
        raise resource_with_id_not_found(str(e))
