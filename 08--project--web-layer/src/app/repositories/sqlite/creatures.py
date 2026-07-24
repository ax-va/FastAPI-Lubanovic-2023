from sqlite3 import Connection, Row

from app.models.schemas.creatures import CreatureRequest, CreatureResponse


def to_response(row: Row) -> CreatureResponse:
    """Converts a tuple returned by a `fetch` function to a model object."""
    return CreatureResponse(**dict(row))


def to_dict(creature: CreatureRequest) -> dict:
    """Converts a Pydantic model to a dictionary."""
    return creature.model_dump()


def get_by_id(
    db_connection: Connection,
    creature_id: int,
) -> CreatureResponse | None:
    query = "SELECT * FROM creatures WHERE id = :id"
    values = {"id": creature_id}
    cursor = db_connection.cursor()
    cursor.execute(query, values)
    row = cursor.fetchone()

    return to_response(row) if row else None


def get_all(db_connection: Connection) -> list[CreatureResponse]:
    query = "SELECT * FROM creatures"
    cursor = db_connection.cursor()
    cursor.execute(query)

    return [to_response(row) for row in cursor.fetchall()]


def create(
    db_connection: Connection,
    creature_request: CreatureRequest,
) -> int:
    query = (
        "INSERT INTO creatures (name, country, area, description, aka) "
        "VALUES (:name, :country, :area, :description, :aka)"
    )
    values = to_dict(creature_request)
    cursor = db_connection.cursor()
    cursor.execute(query, values)

    created_id: int | None = cursor.lastrowid
    if created_id is None:
        raise RuntimeError(f"Creature ID was not returned")

    return created_id


def replace(
    db_connection: Connection,
    creature_id: int,
    creature_request: CreatureRequest,
) -> None:
    query = (
        "UPDATE creatures "
        "SET name = :name, "
        "    country = :country, "
        "    area = :area, "
        "    description = :description, "
        "    aka = :aka "
        "WHERE id = :creature_id"
    )
    values = to_dict(creature_request)
    values["creature_id"] = creature_id
    cursor = db_connection.cursor()
    cursor.execute(query, values)

    if cursor.rowcount == 0:
        raise RuntimeError(f"Creature with ID {creature_id} not updated")


def delete(
    db_connection: Connection,
    creature_id: int,
) -> None:
    query = "DELETE FROM creatures WHERE id = :id"
    values = {"id": creature_id}
    cursor = db_connection.cursor()
    cursor.execute(query, values)

    if cursor.rowcount == 0:
        raise RuntimeError(f"Creature with ID {creature_id} not deleted")
