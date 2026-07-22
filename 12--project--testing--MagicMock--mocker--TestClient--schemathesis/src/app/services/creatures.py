from sqlite3 import Connection

from app.models.creatures import CreatureRequest, CreatureResponse
from app.repositories.sqlite import creatures
from app.services.errors import NotFoundError

repository = creatures


def get_all(connection: Connection) -> list[CreatureResponse]:
    return repository.get_all(connection)


def get_by_id(
    connection: Connection,
    creature_id: int,
) -> CreatureResponse | None:
    return repository.get_by_id(connection, creature_id)


def create(
    connection: Connection,
    creature: CreatureRequest,
) -> CreatureResponse:
    try:
        creature_id: int = repository.create(connection, creature)

        created: CreatureResponse | None = get_by_id(connection, creature_id)
        if created is None:
            raise RuntimeError(f"Creature with ID {creature_id} could not be retrieved after creation")

    except Exception:
        connection.rollback()
        raise

    connection.commit()

    return created


def replace(
    connection: Connection,
    creature_id: int,
    creature: CreatureRequest,
) -> CreatureResponse:
    try:
        to_update: CreatureResponse | None = get_by_id(connection, creature_id)
        if to_update is None:
            raise NotFoundError(f"Creature with ID {creature_id} not found")

        repository.replace(connection, creature_id, creature)

        updated: CreatureResponse | None = get_by_id(connection, creature_id)
        if updated is None:
            raise RuntimeError(f"Creature with ID {creature_id} could not be retrieved after update")

    except Exception:
        connection.rollback()
        raise

    connection.commit()

    return updated


def delete(
    connection: Connection,
    creature_id: int,
) -> None:
    try:
        to_delete: CreatureResponse | None = repository.get_by_id(connection, creature_id)
        if to_delete is None:
            raise NotFoundError(f"Creature with ID {creature_id} not found")

        repository.delete(connection, creature_id)

    except Exception:
        connection.rollback()
        raise

    connection.commit()
