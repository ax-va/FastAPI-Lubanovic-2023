from typing import Annotated, Generator

from fastapi import Depends
from sqlalchemy.orm.session import Session

from app.repositories.sqlalchemy import database as db


# dependency
def get_session() -> Generator[Session, None, None]:
    """Provides a database session for a unit of work and close it afterwards."""
    with db.SessionFactory() as db_session:
        yield db_session


DatabaseSession = Annotated[
    Session,
    Depends(get_session),
]
