from fastapi import APIRouter, HTTPException, Depends

from app.models.creatures import CreatureRequest, CreatureResponse
from app.models.users import UserResponse
from app.repositories.errors import NotFoundError
from app.services import creatures
from app.web.deps.auth import get_current_user

service = creatures
router = APIRouter(prefix="/creatures", tags=["Creatures"])


# public API
@router.get("")
@router.get("/")
def get_all() -> list[CreatureResponse]:
    return service.get_all()


# public API
@router.get("/{creature_id}")
@router.get("/{creature_id}/")
def get_by_id(creature_id: int) -> CreatureResponse:
    creature = service.get_by_id(creature_id)
    if creature is None:
        raise HTTPException(
            status_code=404,
            detail=f"Creature with ID {creature_id} not found",
        )

    return creature


# API for only authenticated users
@router.post("")
@router.post("/")
def create(
    creature: CreatureRequest,
    user: UserResponse = Depends(get_current_user),
) -> CreatureResponse:
    return service.create(creature)


# API for only authenticated users
@router.put("/{creature_id}")
@router.put("/{creature_id}/")
def replace(
    creature_id: int,
    creature: CreatureRequest,
    user: UserResponse = Depends(get_current_user),
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
@router.patch("/{creature_id}/")
def modify(creature_id: int) -> CreatureResponse | None:
    raise NotImplementedError()


# API for only authenticated users
@router.delete("/{creature_id}")
@router.delete("/{creature_id}/")
def delete(
    creature_id: int,
    user: UserResponse = Depends(get_current_user),
) -> bool:
    deleted = service.delete(creature_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Creature with ID {creature_id} not found",
        )

    return deleted
