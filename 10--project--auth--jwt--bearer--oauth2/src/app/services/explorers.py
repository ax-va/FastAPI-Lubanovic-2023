from sqlite3 import Connection

from app.models.schemas.explorers import ExplorerRequest, ExplorerResponse
from app.repositories.sqlite import explorers as explorers_repository
from app.services.errors import NotFoundError

repository = explorers_repository


def get_all(db_connection: Connection,) -> list[ExplorerResponse]:
    return repository.get_all(db_connection)


def get_by_id(
    db_connection: Connection,
    explorer_id: int,
) -> ExplorerResponse | None:
    return repository.get_by_id(db_connection, explorer_id)


def create(
    db_connection: Connection,
    explorer_request: ExplorerRequest,
) -> ExplorerResponse:
    try:
        created_id: int = repository.create(db_connection, explorer_request)

        created: ExplorerResponse | None = get_by_id(db_connection, created_id)
        if created is None:
            raise RuntimeError(f"Explorer with ID {created_id} could not be retrieved after creation")

    except Exception:
        db_connection.rollback()
        raise

    db_connection.commit()

    return created


def replace(
    db_connection: Connection,
    explorer_id: int,
    explorer_request: ExplorerRequest,
) -> ExplorerResponse:
    try:
        to_update: ExplorerResponse | None = get_by_id(db_connection, explorer_id)
        if to_update is None:
            raise NotFoundError(f"Explorer with ID {explorer_id} not found")

        repository.replace(db_connection, explorer_id, explorer_request)

        updated: ExplorerResponse | None = get_by_id(db_connection, explorer_id)
        if updated is None:
            raise RuntimeError(f"Explorer with ID {explorer_id} could not be retrieved after update")

    except Exception:
        db_connection.rollback()
        raise

    db_connection.commit()

    return updated


def delete(
    db_connection: Connection,
    explorer_id: int,
) -> None:
    try:
        to_delete: ExplorerResponse | None = get_by_id(db_connection, explorer_id)
        if to_delete is None:
            raise NotFoundError(f"Explorer with ID {explorer_id} not found")

        repository.delete(db_connection, explorer_id)

    except Exception:
        db_connection.rollback()
        raise

    db_connection.commit()
