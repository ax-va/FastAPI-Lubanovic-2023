from collections.abc import Generator
from sqlite3 import Connection

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.models.users import UserResponse
from app.web import creatures as creatures_web
from app.web import explorers as explorers_web
from app.web.deps.auth import get_current_user
from app.web.deps.database import get_connection


@pytest.fixture
def test_app(
    db_connection: Connection,
) -> Generator[FastAPI, None, None]:
    app = FastAPI()
    app.include_router(creatures_web.router)
    app.include_router(explorers_web.router)

    def fake_connection() -> Generator[Connection, None, None]:
        yield db_connection

    # Add to the `dependency_overrides` dictionary
    app.dependency_overrides[get_connection] = fake_connection

    yield app

    # Pop from the `dependency_overrides` dictionary
    app.dependency_overrides.pop(get_connection, None)


@pytest.fixture
def public_client(
    test_app: FastAPI,
) -> Generator[TestClient, None, None]:
    with TestClient(test_app) as client:
        yield client


@pytest.fixture
def user_client(
    test_app: FastAPI,
) -> Generator[TestClient, None, None]:
    def fake_current_user() -> UserResponse:
        return UserResponse(
            id=1,
            username="test",
            is_active=True,
            is_admin=False,
        )

    # Add to the `dependency_overrides` dictionary
    test_app.dependency_overrides[get_current_user] = fake_current_user

    with TestClient(test_app) as client:
        # Authentication is bypassed by overriding `get_current_user`.
        # Requests don't require an Authorization header or JWT token.
        yield client

    # Pop from the `dependency_overrides` dictionary
    test_app.dependency_overrides.pop(get_current_user, None)
