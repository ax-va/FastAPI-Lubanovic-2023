from app.models.creatures import CreatureRequest, CreatureResponse
from app.repositories.errors import NotFoundError
from . import database as db


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


def get_by_id(creature_id: int) -> CreatureResponse | None:
    query = "SELECT * FROM creatures WHERE id=:id"
    values = {"id": creature_id}
    cursor = db.conn.cursor()
    cursor.execute(query, values)
    row = cursor.fetchone()

    return to_model(row) if row else None


def get_all() -> list[CreatureResponse]:
    query = "SELECT * FROM creatures"
    cursor = db.conn.cursor()
    cursor.execute(query)
    rows = list(cursor.fetchall())

    return [to_model(row) for row in rows]


def create(creature: CreatureRequest) -> CreatureResponse:
    query = (
        "INSERT INTO creatures (name, country, area, description, aka) "
        "VALUES (:name, :country, :area, :description, :aka)"
    )
    values = to_dict(creature)
    cursor = db.conn.cursor()
    cursor.execute(query, values)
    db.conn.commit()

    inserted_id: int | None = cursor.lastrowid
    if inserted_id is None:
        raise RuntimeError(f"Inserted creature id was not returned")

    inserted: CreatureResponse | None = get_by_id(inserted_id)
    if inserted is None:
        raise RuntimeError(f"Inserted creature with id={inserted_id} could not be retrieved")

    return inserted


def replace(creature_id: int, creature: CreatureRequest) -> CreatureResponse:
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
    cursor = db.conn.cursor()
    cursor.execute(query, values)

    if cursor.rowcount == 0:
        raise NotFoundError(f"Creature with id={creature_id} not found")

    db.conn.commit()

    updated: CreatureResponse | None = get_by_id(creature_id)
    if updated is None:
        raise RuntimeError(f"Updated creature with id={creature_id} could not be retrieved")

    return updated


def delete(creature_id: int) -> bool:
    query = "DELETE FROM creatures WHERE id = :id"
    values = {"id": creature_id}
    cursor = db.conn.cursor()
    cursor.execute(query, values)
    deleted: int = cursor.rowcount
    db.conn.commit()

    return deleted > 0
