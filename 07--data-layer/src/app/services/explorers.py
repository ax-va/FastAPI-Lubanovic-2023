from app.models.explorer import Explorer
from app.repositories.sqlite import explorers

repository = explorers


def get_all() -> list[Explorer]:
    return repository.get_all()


def get_one(explorer_id: int) -> Explorer | None:
    return repository.get_one(explorer_id)


def create(explorer: Explorer) -> Explorer:
    return repository.create(explorer)


def replace(explorer_id: int, explorer: Explorer) -> Explorer:
    return repository.replace(explorer_id, explorer)


def delete(explorer_id: int) -> bool:
    return repository.delete(explorer_id)
