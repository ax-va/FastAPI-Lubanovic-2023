from sqlite3 import Connection
from typing import Annotated

from fastapi import Depends

from app.repositories.sqlite.database import get_connection

DatabaseConnection = Annotated[
    Connection,
    Depends(get_connection),
]
