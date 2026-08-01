from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine

# Import all ORM models to create tables by `create_all` later
import app.models.orm  # noqa: F401
from app.config import DATABASE_FILE


DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

# SQLAlchemy engine:
# 1) Stores the database configuration and connection URL;
# 2) Creates and manages database connections;
# 3) Reuses connections through a connection pool;
# 4) Provides connections to SQLAlchemy sessions.
engine: Engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# Create tables if they don't exist
SQLModel.metadata.create_all(engine)
