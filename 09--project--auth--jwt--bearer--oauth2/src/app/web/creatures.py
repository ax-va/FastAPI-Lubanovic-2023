from fastapi import APIRouter, HTTPException, Depends

from app.models.creatures import CreatureRequest, CreatureResponse
from app.models.users import UserResponse
from app.services import creatures
from app.services.errors import NotFoundError
from app.web.deps.auth import get_current_user
from app.web.errors import resource_with_id_not_found

service = creatures
router = APIRouter(prefix="/creatures", tags=["Creatures"])


# public API
@router.get("")
def get_all() -> list[CreatureResponse]:
    return service.get_all()


# public API
@router.get("/{creature_id}")
def get_by_id(creature_id: int) -> CreatureResponse:
    creature = service.get_by_id(creature_id)

    if creature is None:
        raise resource_with_id_not_found(f"Creature with ID {creature_id} not found")

    return creature


# API for only authenticated users
@router.post("", status_code=201)  # 201 Created
def create(
    creature: CreatureRequest,
    _: UserResponse = Depends(get_current_user),
) -> CreatureResponse:
    return service.create(creature)


# API for only authenticated users
@router.put("/{creature_id}")
def replace(
    creature_id: int,
    creature: CreatureRequest,
    _: UserResponse = Depends(get_current_user),
) -> CreatureResponse:
    try:
        creature = service.replace(creature_id, creature)

    except NotFoundError as e:
        raise resource_with_id_not_found(str(e))

    return creature


@router.patch("/{creature_id}")
def modify(creature_id: int) -> CreatureResponse | None:
    raise NotImplementedError()


# API for only authenticated users
@router.delete("/{creature_id}")
def delete(
    creature_id: int,
    _: UserResponse = Depends(get_current_user),
) -> None:
    try:
        service.delete(creature_id)

    except NotFoundError as e:
        raise resource_with_id_not_found(str(e))
