from sqlite3 import Connection

from app.models.creatures import CreatureRequest, CreatureResponse


def to_model(row: tuple) -> CreatureResponse:
    """Converts a tuple returned by a `fetch` function to a model object."""
    creature_id, name, country, area, description, aka = row
    return CreatureResponse(
        id=creature_id,
        name=name,
        country=country,
        area=area,
        description=description,
        aka=aka,
    )


def to_dict(creature: CreatureRequest) -> dict:
    """Converts a Pydantic model to a dictionary."""
    return creature.model_dump()


def get_by_id(
    connection: Connection,
    creature_id: int,
) -> CreatureResponse | None:
    query = "SELECT * FROM creatures WHERE id = :id"
    values = {"id": creature_id}
    cursor = connection.cursor()
    cursor.execute(query, values)
    row = cursor.fetchone()

    return to_model(row) if row else None


def get_all(connection: Connection) -> list[CreatureResponse]:
    query = "SELECT * FROM creatures"
    cursor = connection.cursor()
    cursor.execute(query)

    return [to_model(row) for row in cursor.fetchall()]


def create(
    connection: Connection,
    creature: CreatureRequest,
) -> int:
    query = (
        "INSERT INTO creatures (name, country, area, description, aka) "
        "VALUES (:name, :country, :area, :description, :aka)"
    )
    values = to_dict(creature)
    cursor = connection.cursor()
    cursor.execute(query, values)

    created_id: int | None = cursor.lastrowid
    if created_id is None:
        raise RuntimeError(f"Creature ID was not returned")

    return created_id


def replace(
    connection: Connection,
    creature_id: int,
    creature: CreatureRequest,
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
    values = to_dict(creature)
    values["creature_id"] = creature_id
    cursor = connection.cursor()
    cursor.execute(query, values)

    if cursor.rowcount == 0:
        raise RuntimeError(f"Creature with ID {creature_id} not updated")


def delete(
    connection: Connection,
    creature_id: int,
) -> None:
    query = "DELETE FROM creatures WHERE id = :id"
    values = {"id": creature_id}
    cursor = connection.cursor()
    cursor.execute(query, values)

    if cursor.rowcount == 0:
        raise RuntimeError(f"Creature with ID {creature_id} not deleted")
