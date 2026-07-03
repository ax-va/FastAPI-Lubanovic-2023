from app.models.explorer import Explorer
from . import database as db


def row_to_model(row: tuple) -> Explorer:
    """Converts a tuple returned by a `fetch` function to a model object."""
    _, name, country, description = row
    return Explorer(
        name=name,
        country=country,
        description=description,
    )


def model_to_dict(explorer: Explorer) -> dict:
    """Converts a Pydantic model to a dictionary."""
    return explorer.model_dump()


def get_one(explorer_id: int) -> Explorer | None:
    query = "SELECT * FROM explorers WHERE id=:id"
    values = {"id": explorer_id}
    cursor = db.conn.cursor()
    cursor.execute(query, values)
    row = cursor.fetchone()

    return row_to_model(row) if row else None


def get_all() -> list[Explorer]:
    query = "SELECT * FROM explorers"
    cursor = db.conn.cursor()
    cursor.execute(query)
    rows = list(cursor.fetchall())
    
    return [row_to_model(row) for row in rows]


def create(explorer: Explorer) -> Explorer:
    query = (
        "INSERT INTO explorers (name, country, area, description, aka) "
        "VALUES (:name, :country, :area, :description, :aka)"
    )
    values = model_to_dict(explorer)
    cursor = db.conn.cursor()
    cursor.execute(query, values)
    db.conn.commit()

    inserted_id: int | None = cursor.lastrowid
    if inserted_id is None:
        raise RuntimeError(f"Inserted explorer id was not returned")

    inserted: Explorer | None = get_one(inserted_id)
    if inserted is None:
        raise RuntimeError(f"Inserted explorer with id={inserted_id} could not be retrieved")

    return inserted


def replace(explorer_id: int, explorer: Explorer) -> Explorer | None:
    query = (
        "UPDATE explorers "
        "SET name=:name, "
        "    country=:country, "
        "    description=:description "
        "WHERE id=:explorer_id"
    )
    values = model_to_dict(explorer)
    values["explorer_id"] = explorer_id
    cursor = db.conn.cursor()
    cursor.execute(query, values)

    if cursor.rowcount == 0:
        return None

    db.conn.commit()

    updated: Explorer | None = get_one(explorer_id)
    if updated is None:
        raise RuntimeError(f"Updated explorer with id={explorer_id} could not be retrieved")

    return updated


def delete(explorer_id: int):
    query = "DELETE FROM explorers WHERE id = :id"
    values = {"id": explorer_id}
    cursor = db.conn.cursor()
    cursor.execute(query, values)
    deleted: int = cursor.rowcount
    db.conn.commit()

    return deleted > 0
