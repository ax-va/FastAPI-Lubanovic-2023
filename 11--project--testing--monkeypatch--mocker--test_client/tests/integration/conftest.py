from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.users import UserResponse
from app.web.deps.auth import get_current_user


@pytest.fixture
def user_client(monkeypatch: pytest.MonkeyPatch) -> Generator[TestClient, None, None]:
    def fake_current_user():
        return UserResponse(
            id=1,
            username="test",
            is_active=True,
            is_admin=False,
        )

    # Add to the `dependency_overrides` dictionary
    app.dependency_overrides[get_current_user] = fake_current_user

    with TestClient(app) as client:
        yield client

    # Pop from the `dependency_overrides` dictionary
    app.dependency_overrides.pop(get_current_user, None)
