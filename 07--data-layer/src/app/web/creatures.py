from fastapi import APIRouter

from app.models.creature import Creature
from app.services import creatures

service = creatures
router = APIRouter(prefix="/creatures")


@router.get("")
def get_all() -> list[Creature]:
    return service.get_all()


@router.get("/{creature_id}")
def get_one(creature_id: int) -> Creature | None:
    return service.get_one(creature_id)


# all the remaining endpoints do nothing yet
@router.post("")
def create(creature: Creature) -> Creature:
    return service.create(creature)


@router.put("")
def replace(creature_id: int, creature: Creature) -> Creature:
    return service.replace(creature_id, creature)


@router.patch("")
def modify(creature_id: int, creature: Creature) -> Creature:
    return service.modify(creature_id, creature)


@router.delete("/{creature_id}")
def delete(creature_id: int) -> bool:
    return service.delete(creature_id)
