from app.models.creature import Creature
from . import _database as db


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
    db.cursor.execute(query, values)
    row = db.cursor.fetchone()
    return row_to_model(row) if row else None


def get_all() -> list[Creature]:
    query = "SELECT * FROM creatures"
    db.cursor.execute(query)
    rows = list(db.cursor.fetchall())
    return [row_to_model(row) for row in rows]


def create(creature: Creature) -> Creature:
    query = (
        "INSERT INTO creatures (name, country, area, description, aka) "
        "VALUES (:name, :country, :area, :description, :aka)"
    )
    values = model_to_dict(creature)
    db.cursor.execute(query, values)
    db.conn.commit()
    return creature


def replace(creature_id: int, creature: Creature) -> Creature:
    return creature


def modify(creature_id: int, creature: Creature) -> Creature:
    return creature


def delete(creature_id: int) -> bool:
    query = "DELETE FROM creatures WHERE id = :id"
    values = {"id": creature_id}
    db.cursor.execute(query, values)
    deleted: int = db.cursor.rowcount
    db.conn.commit()

    return deleted > 0
