from app.models.creatures import CreatureRequest, CreatureResponse
from app.repositories.sqlite import creatures
from app.services.errors import NotFoundError

repository = creatures


def get_all() -> list[CreatureResponse]:
    return repository.get_all()


def get_by_id(creature_id: int) -> CreatureResponse | None:
    return repository.get_by_id(creature_id)


def create(creature: CreatureRequest) -> CreatureResponse:
    creature_id: int = repository.create(creature)

    created: CreatureResponse | None = get_by_id(creature_id)
    if created is None:
        raise RuntimeError(f"Creature with ID {creature_id} could not be retrieved after creation")

    return created


def replace(creature_id: int, creature: CreatureRequest) -> CreatureResponse:
    to_update: CreatureResponse | None = get_by_id(creature_id)
    if to_update is None:
        raise NotFoundError(f"Creature with ID {creature_id} not found")

    repository.replace(creature_id, creature)

    updated: CreatureResponse | None = get_by_id(creature_id)
    if updated is None:
        raise RuntimeError(f"Creature with ID {creature_id} could not be retrieved after update")

    return updated


def delete(creature_id: int) -> None:
    to_delete: CreatureResponse | None = repository.get_by_id(creature_id)
    if to_delete is None:
        raise NotFoundError(f"Creature with ID {creature_id} not found")

    repository.delete(creature_id)
