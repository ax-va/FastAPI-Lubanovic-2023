from sqlite3 import Connection

import pytest
from fastapi.testclient import TestClient

from app.models.explorers import ExplorerRequest, ExplorerResponse
from tests.samples.explorers import (
    hande_response,
    weiser_response,
    ax_va_request,
    ax_va_response,
)


@pytest.mark.parametrize(
    "sample_request, sample_response",
    [
        (ax_va_request, ax_va_response),
    ]
)
def test_create(
    sample_request: ExplorerRequest,
    sample_response: ExplorerResponse,
    db_connection: Connection,
    user_client: TestClient,
) -> None:

    payload = sample_request.model_dump()

    # Authentication is bypassed by overriding `get_current_user`.
    # Requests don't require an Authorization header or JWT token.
    response = user_client.post("/explorers", json=payload)

    assert response.status_code == 201
    assert response.json() == sample_response.model_dump()


@pytest.mark.positive
@pytest.mark.parametrize(
    "sample_id, sample_response",
    [
        (1, hande_response),
        (2, weiser_response),
    ]
)
def test_get_by_id_success(
    sample_id: int,
    sample_response: ExplorerResponse,
    db_connection: Connection,
    public_client: TestClient,
):
    response = public_client.get(f"/explorers/{sample_id}")

    assert response.status_code == 200
    assert response.json() == sample_response.model_dump()


@pytest.mark.negative
@pytest.mark.parametrize(
    "sample_id", [99]
)
def test_get_by_id_not_found(
    sample_id: int,
    db_connection: Connection,
    public_client: TestClient,
):
    response = public_client.get(f"/explorers/{sample_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == f"Explorer with ID {sample_id} not found"
