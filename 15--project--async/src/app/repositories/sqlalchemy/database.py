from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlmodel import SQLModel, create_engine

# Import all ORM models to create tables by `create_all` later
import app.models.orm  # noqa: F401
from app.config import DATABASE_FILE

SYNC_DATABASE_URL = f"sqlite:///{DATABASE_FILE}"
ASYNC_DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_FILE}"

# Synchronous engine used only for schema management (creating database tables)
sync_engine: Engine = create_engine(
    SYNC_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
# Asynchronous engine used for all database queries
async_engine: AsyncEngine = create_async_engine(
    ASYNC_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# Create database tables once during application startup if they don't exist
SQLModel.metadata.create_all(sync_engine)

async_session_factory = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
