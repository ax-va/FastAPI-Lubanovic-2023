from fastapi import APIRouter

from app.fake import creature_repository
from app.models.creature import Creature

router = APIRouter(prefix="/creatures")


@router.get("")
def get_all() -> list[Creature]:
    return creature_repository.get_all()


@router.get("/{creature_id}")
def get_one(creature_id: int) -> Creature | None:
    return creature_repository.get_one(creature_id)


# all the remaining endpoints do nothing yet
@router.post("")
def create(creature: Creature) -> Creature:
    return creature_repository.create(creature)


@router.put("")
def replace(creature: Creature) -> Creature:
    return creature_repository.replace(creature)


@router.patch("")
def modify(creature: Creature) -> Creature:
    return creature_repository.modify(creature)


@router.delete("/{creature_id}")
def delete(creature_id: int) -> bool:
    return creature_repository.delete(creature_id)
