from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import DATABASE_FILE


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""


def make_sqlite_url(database_file: str | Path) -> str:
    """Builds a SQLAlchemy URL for a SQLite database."""
    return f"sqlite:///{Path(database_file)}"


DATABASE_URL = make_sqlite_url(DATABASE_FILE)

# SQLAlchemy Engine:
# 1) Stores the database configuration and connection URL;
# 2) Creates and manages database connections;
# 3) Reuses connections through a connection pool;
# 4) Provides connections to SQLAlchemy sessions.
engine: Engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# SQLAlchemy Session Factory:
# 1) Stores the configuration for creating sessions;
# 2) Creates a new independent `Session` object on each call;
# 3) Binds every session to the configured Engine.
SessionFactory = sessionmaker(
    bind=engine,
    # Doesn't automatically flush pending changes before SQL queries.
    # Pending changes remain only in the session
    # until `session.flush()` or `session.commit()` is called.
    autoflush=False,
    # Keep ORM objects usable after `session.commit()`
    # without lazily reloading their attributes from the database.
    expire_on_commit=False,
)


def get_session() -> Generator[Session, None, None]:
    """Provides a database session for a unit of work and close it afterwards."""
    with SessionFactory() as session:
        yield session
