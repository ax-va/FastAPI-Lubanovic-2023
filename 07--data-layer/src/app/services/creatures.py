from app.models.creature import Creature
from app.repositories.sqlite import creatures

repository = creatures


def get_all() -> list[Creature]:
    return repository.get_all()


def get_one(creature_id: int) -> Creature | None:
    return repository.get_one(creature_id)


def create(creature: Creature) -> Creature:
    return repository.create(creature)


def replace(creature_id: int, creature: Creature) -> Creature | None:
    return repository.replace(creature_id, creature)


def delete(creature_id: int) -> bool:
    return repository.delete(creature_id)
