from app.models.creatures import CreatureRequest, CreatureResponse
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
    query = "SELECT * FROM creatures WHERE id = :id"
    values = {"id": creature_id}
    cursor = db.conn.cursor()
    cursor.execute(query, values)
    row = cursor.fetchone()

    return to_model(row) if row else None


def get_all() -> list[CreatureResponse]:
    query = "SELECT * FROM creatures"
    cursor = db.conn.cursor()
    cursor.execute(query)

    return [to_model(row) for row in cursor.fetchall()]


def create(creature: CreatureRequest) -> int:
    query = (
        "INSERT INTO creatures (name, country, area, description, aka) "
        "VALUES (:name, :country, :area, :description, :aka)"
    )
    values = to_dict(creature)
    cursor = db.conn.cursor()
    cursor.execute(query, values)

    created_id: int | None = cursor.lastrowid
    if created_id is None:
        db.conn.rollback()
        raise RuntimeError(f"Creature ID was not returned")

    db.conn.commit()

    return created_id


def replace(creature_id: int, creature: CreatureRequest) -> None:
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
        db.conn.rollback()
        raise RuntimeError(f"Creature with ID {creature_id} not updated")

    db.conn.commit()


def delete(creature_id: int) -> None:
    query = "DELETE FROM creatures WHERE id = :id"
    values = {"id": creature_id}
    cursor = db.conn.cursor()
    cursor.execute(query, values)

    if cursor.rowcount == 0:
        db.conn.rollback()
        raise RuntimeError(f"Creature with ID {creature_id} not deleted")

    db.conn.commit()
