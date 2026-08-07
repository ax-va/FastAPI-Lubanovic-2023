from collections.abc import AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.schemas.users import UserResponse
from app.web import creatures as creatures_web
from app.web import explorers as explorers_web
from app.web.deps.auth import get_current_user
from app.web.deps.database import get_session


@pytest.fixture
async def test_app(
    db_session: AsyncSession,
) -> AsyncGenerator[FastAPI, None]:
    app = FastAPI()
    app.include_router(creatures_web.router)
    app.include_router(explorers_web.router)

    async def fake_session() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    # Add to the `dependency_overrides` dictionary
    app.dependency_overrides[get_session] = fake_session

    try:
        yield app
    finally:
        # Pop from the `dependency_overrides` dictionary
        app.dependency_overrides.pop(get_session, None)


@pytest.fixture
async def public_client(
    test_app: FastAPI,
) -> AsyncGenerator[AsyncClient, None]:
    # `ASGITransport` routes requests directly to
    # the FastAPI application without opening real network connections.
    # This allows `AsyncClient` to test the application entirely in memory.
    transport = ASGITransport(app=test_app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client


@pytest.fixture
async def user_client(
    test_app: FastAPI,
) -> AsyncGenerator[AsyncClient, None]:
    def fake_current_user() -> UserResponse:
        return UserResponse(
            id=1,
            username="test",
            is_active=True,
            is_admin=False,
        )

    # Add to the `dependency_overrides` dictionary
    test_app.dependency_overrides[get_current_user] = fake_current_user

    # `ASGITransport` routes requests directly to
    # the FastAPI application without opening real network connections.
    # This allows `AsyncClient` to test the application entirely in memory.
    transport = ASGITransport(app=test_app)

    try:
        async with AsyncClient(
            transport=transport,
            base_url="http://test",
        ) as client:
            # Authentication is bypassed by overriding `get_current_user`.
            # Requests don't require an Authorization header or JWT token.
            yield client
    finally:
        # Pop from the `dependency_overrides` dictionary
        test_app.dependency_overrides.pop(get_current_user, None)
