from app.models.explorers import ExplorerRequest, ExplorerResponse
from . import database as db


def to_model(row: tuple) -> ExplorerResponse:
    """Converts a tuple returned by a `fetch` function to a model object."""
    explorer_id, name, country, description = row
    return ExplorerResponse(
        id=explorer_id,
        name=name,
        country=country,
        description=description,
    )


def to_dict(explorer: ExplorerRequest) -> dict:
    """Converts a Pydantic model to a dictionary."""
    return explorer.model_dump()


def get_by_id(explorer_id: int) -> ExplorerResponse | None:
    query = "SELECT * FROM explorers WHERE id = :id"
    values = {"id": explorer_id}
    cursor = db.conn.cursor()
    cursor.execute(query, values)
    row = cursor.fetchone()

    return to_model(row) if row else None


def get_all() -> list[ExplorerResponse]:
    query = "SELECT * FROM explorers"
    cursor = db.conn.cursor()
    cursor.execute(query)

    return [to_model(row) for row in cursor.fetchall()]


def create(explorer: ExplorerRequest) -> int:
    query = (
        "INSERT INTO explorers (name, country, description) "
        "VALUES (:name, :country, :description)"
    )
    values = to_dict(explorer)
    cursor = db.conn.cursor()
    cursor.execute(query, values)

    creature_id: int | None = cursor.lastrowid
    if creature_id is None:
        db.conn.rollback()
        raise RuntimeError(f"Explorer ID was not returned")

    db.conn.commit()

    return creature_id


def replace(explorer_id: int, explorer: ExplorerRequest) -> None:
    query = (
        "UPDATE explorers "
        "SET name=:name, "
        "    country=:country, "
        "    description=:description "
        "WHERE id=:explorer_id"
    )
    values = to_dict(explorer)
    values["explorer_id"] = explorer_id
    cursor = db.conn.cursor()
    cursor.execute(query, values)

    if cursor.rowcount == 0:
        db.conn.rollback()
        raise RuntimeError(f"Explorer with ID {explorer_id} not updated")

    db.conn.commit()


def delete(explorer_id: int) -> None:
    query = "DELETE FROM explorers WHERE id = :id"
    values = {"id": explorer_id}
    cursor = db.conn.cursor()
    cursor.execute(query, values)

    if cursor.rowcount == 0:
        db.conn.rollback()
        raise RuntimeError(f"Explorer with ID {explorer_id} not deleted")

    db.conn.commit()
