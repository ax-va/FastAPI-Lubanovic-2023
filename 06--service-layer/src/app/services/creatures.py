from typing import Any

from app.models.creature import Creature
from app.repositories import fake_creatures

repository = fake_creatures


def get_all() -> list[Creature]:
    return repository.get_all()


def get_one(creature_id: int) -> Creature | None:
    return repository.get(creature_id)


def create(creature: Creature) -> Creature:
    return repository.create(creature)


def replace(creature_id: int, creature: Creature) -> Creature:
    return repository.replace(creature_id, creature)


def modify(creature_id: int, creature: Creature) -> Creature:
    return repository.modify(creature_id, creature)


def delete(creature_id: int) -> bool:
    return repository.delete(creature_id)
