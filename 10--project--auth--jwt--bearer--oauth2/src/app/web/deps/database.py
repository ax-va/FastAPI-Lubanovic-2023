from sqlite3 import Connection
from typing import Annotated, Generator

from fastapi import Depends

from app.config import DATABASE_FILE
from app.repositories.sqlite.database import connection_manager


# dependency
def get_connection(
    database_file: str = DATABASE_FILE,
) -> Generator[Connection, None, None]:
    """Provides a database connection for a unit of work and close it afterwards."""
    with connection_manager(database_file) as connection:
        yield connection


DatabaseConnection = Annotated[
    Connection,
    Depends(get_connection),
]
