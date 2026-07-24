from sqlite3 import Connection

from app.models.schemas.creatures import CreatureRequest, CreatureResponse
from app.repositories.sqlite import creatures as creatures_repository
from app.services.errors import NotFoundError

repository = creatures_repository


def get_all(db_connection: Connection) -> list[CreatureResponse]:
    return repository.get_all(db_connection)


def get_by_id(
    db_connection: Connection,
    creature_id: int,
) -> CreatureResponse | None:
    return repository.get_by_id(db_connection, creature_id)


def create(
    db_connection: Connection,
    creature_request: CreatureRequest,
) -> CreatureResponse:
    try:
        creature_id: int = repository.create(db_connection, creature_request)

        created: CreatureResponse | None = get_by_id(db_connection, creature_id)
        if created is None:
            raise RuntimeError(f"Creature with ID {creature_id} could not be retrieved after creation")

    except Exception:
        db_connection.rollback()
        raise

    db_connection.commit()

    return created


def replace(
    db_connection: Connection,
    creature_id: int,
    creature_request: CreatureRequest,
) -> CreatureResponse:
    try:
        to_update: CreatureResponse | None = get_by_id(db_connection, creature_id)
        if to_update is None:
            raise NotFoundError(f"Creature with ID {creature_id} not found")

        repository.replace(db_connection, creature_id, creature_request)

        updated: CreatureResponse | None = get_by_id(db_connection, creature_id)
        if updated is None:
            raise RuntimeError(f"Creature with ID {creature_id} could not be retrieved after update")

    except Exception:
        db_connection.rollback()
        raise

    db_connection.commit()

    return updated


def delete(
    db_connection: Connection,
    creature_id: int,
) -> None:
    try:
        to_delete: CreatureResponse | None = get_by_id(db_connection, creature_id)
        if to_delete is None:
            raise NotFoundError(f"Creature with ID {creature_id} not found")

        repository.delete(db_connection, creature_id)

    except Exception:
        db_connection.rollback()
        raise

    db_connection.commit()
