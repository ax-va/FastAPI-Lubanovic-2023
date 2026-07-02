from app.models.explorer import Explorer
from . import _database as db


def row_to_model(row: tuple) -> Explorer:
    """Converts a tuple returned by a `fetch` function to a model object."""
    _, name, description, country, area, aka = row
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
    db.cursor.execute(query, values)
    row = db.cursor.fetchone()
    return row_to_model(row) if row else None


def get_all() -> list[Explorer]:
    query = "SELECT * FROM explorers"
    db.cursor.execute(query)
    rows = list(db.cursor.fetchall())
    return [row_to_model(row) for row in rows]


def create(explorer: Explorer) -> Explorer:
    query = (
        "INSERT INTO explorers (name, country, area, description, aka) "
        "VALUES (:name, :country, :area, :description, :aka)"
    )
    values = model_to_dict(explorer)
    db.cursor.execute(query, values)
    db.conn.commit()
    return explorer


def replace(explorer_id: int, explorer: Explorer) -> Explorer:
    return explorer


def modify(explorer_id: int, explorer: Explorer) -> Explorer:
    return explorer


def delete(explorer_id: int):
    query = "DELETE FROM explorers WHERE id = :id"
    values = {"id": explorer_id}
    db.cursor.execute(query, values)
    deleted: int = db.cursor.rowcount
    db.conn.commit()

    return deleted > 0
