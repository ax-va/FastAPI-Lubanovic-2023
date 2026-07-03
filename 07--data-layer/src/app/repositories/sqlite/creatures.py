from app.models.creature import Creature
from . import database as db


def row_to_model(row: tuple) -> Creature:
    """Converts a tuple returned by a `fetch` function to a model object."""
    _, name, country, area, description, aka = row
    return Creature(
        name=name,
        country=country,
        area=area,
        description=description,
        aka=aka,
    )


def model_to_dict(creature: Creature) -> dict:
    """Converts a Pydantic model to a dictionary."""
    return creature.model_dump()


def get_one(creature_id: int) -> Creature | None:
    query = "SELECT * FROM creatures WHERE id=:id"
    values = {"id": creature_id}
    cursor = db.conn.cursor()
    cursor.execute(query, values)
    row = cursor.fetchone()

    return row_to_model(row) if row else None


def get_all() -> list[Creature]:
    query = "SELECT * FROM creatures"
    cursor = db.conn.cursor()
    cursor.execute(query)
    rows = list(cursor.fetchall())

    return [row_to_model(row) for row in rows]


def create(creature: Creature) -> Creature:
    query = (
        "INSERT INTO creatures (name, country, area, description, aka) "
        "VALUES (:name, :country, :area, :description, :aka)"
    )
    values = model_to_dict(creature)
    cursor = db.conn.cursor()
    cursor.execute(query, values)
    db.conn.commit()

    inserted_id: int | None = cursor.lastrowid
    if inserted_id is None:
        raise RuntimeError(f"Inserted creature id was not returned")

    inserted: Creature | None = get_one(inserted_id)
    if inserted is None:
        raise RuntimeError(f"Inserted creature with id={inserted_id} could not be retrieved")

    return inserted


def replace(creature_id: int, creature: Creature) -> Creature | None:
    query = (
        "UPDATE creatures "
        "SET name=:name, "
        "    country=:country, "
        "    area=:area, "
        "    description=:description, "
        "    aka=:aka "
        "WHERE id=:creature_id"
    )
    values = model_to_dict(creature)
    values["creature_id"] = creature_id
    cursor = db.conn.cursor()
    cursor.execute(query, values)

    if cursor.rowcount == 0:
        return None

    db.conn.commit()

    updated: Creature | None = get_one(creature_id)
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
