from collections.abc import Generator
from sqlite3 import Connection
from typing import Annotated

from fastapi import Depends

from app.repositories.sqlite import database as db


# dependency
def get_connection() -> Generator[Connection, None, None]:
    """Provides a database connection for a unit of work and close it afterwards."""
    with db.connect() as db_connection:
        yield db_connection


DatabaseConnection = Annotated[
    Connection,
    Depends(get_connection),
]
