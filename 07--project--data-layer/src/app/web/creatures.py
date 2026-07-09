from fastapi import APIRouter, HTTPException

from app.models.creatures import CreatureRequest, CreatureResponse
from app.repositories.errors import NotFoundError
from app.services import creatures

service = creatures
router = APIRouter(prefix="/creatures", tags=["Creatures"])


@router.get("")
@router.get("/")
def get_all() -> list[CreatureResponse]:
    return service.get_all()


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


@router.post("", status_code=201)  # 201 Created
@router.post("/", status_code=201)  # 201 Created
def create(creature: CreatureRequest) -> CreatureResponse:
    return service.create(creature)


@router.put("/{creature_id}")
@router.put("/{creature_id}/")
def replace(creature_id: int, creature: CreatureRequest) -> CreatureResponse:
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
def modify(creature_id: int) -> CreatureResponse:
    raise NotImplementedError()


@router.delete("/{creature_id}")
@router.delete("/{creature_id}/")
def delete(creature_id: int) -> bool:
    deleted = service.delete(creature_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Creature with ID {creature_id} not found",
        )

    return deleted
