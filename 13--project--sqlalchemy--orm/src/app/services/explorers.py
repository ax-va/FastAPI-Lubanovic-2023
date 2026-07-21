from app.models.explorers import ExplorerRequest, ExplorerResponse
from app.repositories.sqlite import explorers
from app.services.errors import NotFoundError

repository = explorers


def get_all() -> list[ExplorerResponse]:
    return repository.get_all()


def get_by_id(explorer_id: int) -> ExplorerResponse | None:
    return repository.get_by_id(explorer_id)


def create(explorer: ExplorerRequest) -> ExplorerResponse:
    created_id: int = repository.create(explorer)

    created: ExplorerResponse | None = get_by_id(created_id)
    if created is None:
        raise RuntimeError(f"Explorer with ID {created_id} could not be retrieved after creation")

    return created


def replace(explorer_id: int, explorer: ExplorerRequest) -> ExplorerResponse:
    to_update = repository.get_by_id(explorer_id)
    if to_update is None:
        raise NotFoundError(f"Explorer with ID {explorer_id} not found")

    repository.replace(explorer_id, explorer)

    updated: ExplorerResponse | None = get_by_id(explorer_id)
    if updated is None:
        raise RuntimeError(f"Explorer with ID {explorer_id} could not be retrieved after update")

    return updated


def delete(explorer_id: int) -> None:
    to_delete = repository.get_by_id(explorer_id)
    if to_delete is None:
        raise NotFoundError(f"Explorer with ID {explorer_id} not found")

    repository.delete(explorer_id)
