from app.models.creatures import CreatureRequest, CreatureResponse
from app.repositories import fake_creatures

repository = fake_creatures


def get_all() -> list[CreatureResponse]:
    return repository.get_all()


def get_one(creature_id: int) -> CreatureResponse | None:
    return repository.get_one(creature_id)


def create(creature: CreatureRequest) -> CreatureResponse:
    return repository.create(creature)


def replace(creature_id: int, creature: CreatureRequest) -> CreatureResponse:
    return repository.replace(creature_id, creature)


def delete(creature_id: int) -> bool:
    return repository.delete(creature_id)
