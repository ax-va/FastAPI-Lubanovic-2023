from sqlite3 import Connection

from app.models.explorers import ExplorerRequest, ExplorerResponse
from app.repositories.sqlite import explorers
from app.services.errors import NotFoundError

repository = explorers


def get_all(connection: Connection,) -> list[ExplorerResponse]:
    return repository.get_all(connection)


def get_by_id(
    connection: Connection,
    explorer_id: int,
) -> ExplorerResponse | None:
    return repository.get_by_id(connection, explorer_id)


def create(
    connection: Connection,
    explorer: ExplorerRequest,
) -> ExplorerResponse:
    try:
        created_id: int = repository.create(connection, explorer)

        created: ExplorerResponse | None = get_by_id(connection, created_id)
        if created is None:
            raise RuntimeError(f"Explorer with ID {created_id} could not be retrieved after creation")

    except Exception:
        connection.rollback()
        raise

    connection.commit()

    return created


def replace(
    connection: Connection,
    explorer_id: int,
    explorer: ExplorerRequest,
) -> ExplorerResponse:
    try:
        to_update = repository.get_by_id(connection, explorer_id)
        if to_update is None:
            raise NotFoundError(f"Explorer with ID {explorer_id} not found")

        repository.replace(connection, explorer_id, explorer)

        updated: ExplorerResponse | None = get_by_id(connection, explorer_id)
        if updated is None:
            raise RuntimeError(f"Explorer with ID {explorer_id} could not be retrieved after update")

    except Exception:
        connection.rollback()
        raise

    connection.commit()

    return updated


def delete(
    connection: Connection,
    explorer_id: int,
) -> None:
    try:
        to_delete = repository.get_by_id(connection, explorer_id)
        if to_delete is None:
            raise NotFoundError(f"Explorer with ID {explorer_id} not found")

        repository.delete(connection, explorer_id)

    except Exception:
        connection.rollback()
        raise

    connection.commit()
