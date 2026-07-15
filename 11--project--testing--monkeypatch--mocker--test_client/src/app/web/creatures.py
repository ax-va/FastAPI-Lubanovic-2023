from fastapi import APIRouter, HTTPException, Depends

from app.models.creatures import CreatureRequest, CreatureResponse
from app.models.users import UserResponse
from app.repositories.errors import NotFoundError
from app.services import creatures
from app.web.deps.auth import get_current_user
from app.web.errors import resource_with_id_not_found
from app.web.metadata import NOT_FOUND

service = creatures
router = APIRouter(prefix="/creatures", tags=["Creatures"])


# public API
@router.get("")
def get_all() -> list[CreatureResponse]:
    return service.get_all()


# public API
@router.get(
    "/{creature_id}",
    responses=NOT_FOUND,
)
def get_by_id(creature_id: int) -> CreatureResponse:
    creature = service.get_by_id(creature_id)

    if creature is None:
        raise resource_with_id_not_found("Creature", creature_id)

    return creature


# API for only authenticated users
@router.post("", status_code=201)  # 201 Created
def create(
    creature: CreatureRequest,
    _: UserResponse = Depends(get_current_user),
) -> CreatureResponse:
    return service.create(creature)


# API for only authenticated users
@router.put(
    "/{creature_id}",
    responses=NOT_FOUND,
)
def replace(
    creature_id: int,
    creature: CreatureRequest,
    _: UserResponse = Depends(get_current_user),
) -> CreatureResponse:
    try:
        creature = service.replace(creature_id, creature)

    except NotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    return creature


@router.patch("/{creature_id}")
def modify(creature_id: int) -> CreatureResponse | None:
    raise NotImplementedError()


# API for only authenticated users
@router.delete(
    "/{creature_id}",
    responses=NOT_FOUND,
)
def delete(
    creature_id: int,
    _: UserResponse = Depends(get_current_user),
) -> bool:
    deleted = service.delete(creature_id)

    if not deleted:
        raise resource_with_id_not_found("Creature", creature_id)

    return deleted
