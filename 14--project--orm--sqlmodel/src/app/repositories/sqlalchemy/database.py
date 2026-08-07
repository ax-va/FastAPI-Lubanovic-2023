from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine

from app.config import DATABASE_FILE

DATABASE_URL = f"sqlite:///{DATABASE_FILE}"


def create_schema(engine: Engine):
    # Import all ORM models before calling `create_all`
    import app.models.orm  # noqa: F401

    # Create database tables once during application startup if they don't exist
    SQLModel.metadata.create_all(engine)


# SQLAlchemy engine:
# 1) Stores the database configuration and connection URL;
# 2) Creates and manages database connections;
# 3) Reuses connections through a connection pool;
# 4) Provides connections to SQLAlchemy sessions.
engine: Engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)
