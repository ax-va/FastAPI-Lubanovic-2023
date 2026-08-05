from collections.abc import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool.impl import StaticPool
from sqlmodel import SQLModel

# Import all ORM models to create tables by `create_all` later
import app.models.orm  # noqa: F401
from app.services import creatures as creatures_service
from app.services import explorers as explorers_service
from app.services import users as users_service
from tests.samples.creatures import yeti_request, bigfoot_request
from tests.samples.explorers import hande_request, weiser_request


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async_engine: AsyncEngine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        # Reuse a single connection
        # so all sessions share the same in-memory database.
        poolclass=StaticPool,
    )

    # Create database schema
    async with async_engine.begin() as conn:
        # noinspection PyTypeChecker
        await conn.run_sync(SQLModel.metadata.create_all)

    # Create session factory
    async_session_factory = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    # Populate the database with sample data
    async with async_session_factory() as session:
        await users_service.create_admin(
            session,
            username="admin",
            password="admin",
        )

        await creatures_service.create(session, yeti_request)
        await creatures_service.create(session, bigfoot_request)

        await explorers_service.create(session, hande_request)
        await explorers_service.create(session, weiser_request)

        yield session

    # Release all engine resources
    await async_engine.dispose()
