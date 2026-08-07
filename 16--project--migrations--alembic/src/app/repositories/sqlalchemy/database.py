from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from app.config import DATABASE_FILE

DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_FILE}"

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
