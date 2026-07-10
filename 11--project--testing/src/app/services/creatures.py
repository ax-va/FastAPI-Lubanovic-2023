from app.models.creatures import CreatureRequest, CreatureResponse
from app.repositories.sqlite import creatures

repository = creatures


def get_all() -> list[CreatureResponse]:
    return repository.get_all()


def get_by_id(creature_id: int) -> CreatureResponse | None:
    return repository.get_by_id(creature_id)


def create(creature: CreatureRequest) -> CreatureResponse:
    return repository.create(creature)


def replace(creature_id: int, creature: CreatureRequest) -> CreatureResponse:
    return repository.replace(creature_id, creature)


def delete(creature_id: int) -> bool:
    return repository.delete(creature_id)
