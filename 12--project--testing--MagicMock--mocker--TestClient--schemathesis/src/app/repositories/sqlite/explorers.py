from sqlite3 import Connection, Row

from app.models.schemas.explorers import ExplorerRequest, ExplorerResponse


def to_response(row: Row) -> ExplorerResponse:
    """Converts a tuple returned by a `fetch` function to a model object."""
    return ExplorerResponse(**dict(row))


def to_dict(explorer: ExplorerRequest) -> dict:
    """Converts a Pydantic model to a dictionary."""
    return explorer.model_dump()


def get_by_id(
    db_connection: Connection,
    explorer_id: int,
) -> ExplorerResponse | None:
    query = "SELECT * FROM explorers WHERE id = :id"
    values = {"id": explorer_id}
    cursor = db_connection.cursor()
    cursor.execute(query, values)
    row = cursor.fetchone()

    return to_response(row) if row else None


def get_all(db_connection: Connection) -> list[ExplorerResponse]:
    query = "SELECT * FROM explorers"
    cursor = db_connection.cursor()
    cursor.execute(query)
    
    return [to_response(row) for row in cursor.fetchall()]


def create(
    db_connection: Connection,
    explorer_request: ExplorerRequest,
) -> int:
    query = (
        "INSERT INTO explorers (name, country, description) "
        "VALUES (:name, :country, :description)"
    )
    values = to_dict(explorer_request)
    cursor = db_connection.cursor()
    cursor.execute(query, values)

    creature_id: int | None = cursor.lastrowid
    if creature_id is None:
        raise RuntimeError(f"Explorer ID was not returned")

    return creature_id


def replace(
    db_connection: Connection,
    explorer_id: int,
    explorer_request: ExplorerRequest,
) -> None:
    query = (
        "UPDATE explorers "
        "SET name=:name, "
        "    country=:country, "
        "    description=:description "
        "WHERE id=:explorer_id"
    )
    values = to_dict(explorer_request)
    values["explorer_id"] = explorer_id
    cursor = db_connection.cursor()
    cursor.execute(query, values)

    if cursor.rowcount == 0:
        raise RuntimeError(f"Explorer with ID {explorer_id} not updated")


def delete(
    db_connection: Connection,
    explorer_id: int,
) -> None:
    query = "DELETE FROM explorers WHERE id = :id"
    values = {"id": explorer_id}
    cursor = db_connection.cursor()
    cursor.execute(query, values)

    if cursor.rowcount == 0:
        raise RuntimeError(f"Explorer with ID {explorer_id} not deleted")
