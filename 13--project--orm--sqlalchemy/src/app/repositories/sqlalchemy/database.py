from sqlalchemy import create_engine
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker

# Import all ORM models to create tables by `create_all` later
import app.models.orm  # noqa: F401
from app.config import DATABASE_FILE
from app.models.orm.base import Base


DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

# SQLAlchemy Engine:
# 1) Stores the database configuration and connection URL;
# 2) Creates and manages database connections;
# 3) Reuses connections through a connection pool;
# 4) Provides connections to SQLAlchemy sessions.
engine: Engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# Create tables if they don't exist
Base.metadata.create_all(engine)

# SQLAlchemy session factory:
# 1) Stores the configuration for creating sessions;
# 2) Creates a new independent `Session` object on each call;
# 3) Binds every session to the configured Engine.
session_factory = sessionmaker(
    bind=engine,
    # Doesn't automatically flush pending changes before SQL queries.
    # Pending changes remain only in the session
    # until `session.flush()` or `session.commit()` is called.
    autoflush=False,
    # Keep ORM objects usable after `session.commit()`
    # without lazily reloading their attributes from the database.
    expire_on_commit=False,
)
