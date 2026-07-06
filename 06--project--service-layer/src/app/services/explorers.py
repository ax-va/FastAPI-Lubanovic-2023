from app.models.explorers import ExplorerRequest, ExplorerResponse
from app.repositories import fake_explorers

repository = fake_explorers


def get_all() -> list[ExplorerResponse]:
    return repository.get_all()


def get_by_id(explorer_id: int) -> ExplorerResponse | None:
    return repository.get_by_id(explorer_id)


def create(explorer: ExplorerRequest) -> ExplorerResponse:
    return repository.create(explorer)


def replace(explorer_id: int, explorer: ExplorerRequest) -> ExplorerResponse:
    return repository.replace(explorer_id, explorer)


def delete(explorer_id: int) -> bool:
    return repository.delete(explorer_id)
