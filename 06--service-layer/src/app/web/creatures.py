from fastapi import APIRouter

from app.models.creature import Creature
from app.services import creatures

service = creatures
router = APIRouter(prefix="/creatures")


@router.get("")
@router.get("/")
def get_all() -> list[Creature]:
    return service.get_all()


@router.get("/{creature_id}")
@router.get("/{creature_id}/")
def get_one(creature_id: int) -> Creature | None:
    return service.get_one(creature_id)


@router.post("")
@router.post("/")
def create(creature: Creature) -> Creature:
    return service.create(creature)


@router.put("/{creature_id}")
@router.put("/{creature_id}/")
def replace(creature_id: int, creature: Creature) -> Creature | None:
    return service.replace(creature_id, creature)


@router.patch("/{creature_id}")
@router.patch("/{creature_id}/")
def modify(creature_id: int) -> Creature:
    raise NotImplementedError()


@router.delete("/{creature_id}")
@router.delete("/{creature_id}/")
def delete(creature_id: int) -> bool:
    return service.delete(creature_id)
