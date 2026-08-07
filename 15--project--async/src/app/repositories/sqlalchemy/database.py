from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlmodel import SQLModel
from app.config import DATABASE_FILE

DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_FILE}"


async def create_schema(engine: AsyncEngine) -> None:
    # Import all ORM models before calling `create_all`
    import app.models.orm  # noqa: F401

    # Create database schema
    async with engine.begin() as conn:
        # noinspection PyTypeChecker
        await conn.run_sync(SQLModel.metadata.create_all)


# Asynchronous engine used for all database queries
async_engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

async_session_factory = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
