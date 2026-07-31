from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.repositories.sqlalchemy import database as db


# dependency
def get_session() -> Generator[Session, None, None]:
    """Provides a database session for a unit of work and close it afterwards."""
    with Session(db.engine) as db_session:
        yield db_session


DatabaseSession = Annotated[
    Session,
    Depends(get_session),
]
