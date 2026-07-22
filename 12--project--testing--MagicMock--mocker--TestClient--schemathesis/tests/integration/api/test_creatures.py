from sqlite3 import Connection

import pytest
from fastapi.testclient import TestClient

from app.models.creatures import CreatureRequest, CreatureResponse
from tests.samples.creatures import (
    yeti_response,
    bigfoot_response,
    lubanovic_request,
    lubanovic_response,
)


@pytest.mark.parametrize(
    "sample_request, sample_response",
    [
        (lubanovic_request, lubanovic_response),
    ]
)
def test_create(
    sample_request: CreatureRequest,
    sample_response: CreatureResponse,
    user_client: TestClient,
) -> None:

    payload = sample_request.model_dump()

    # Authentication is bypassed by overriding `get_current_user`.
    # Requests don't require an Authorization header or JWT token.
    response = user_client.post("/creatures", json=payload)

    assert response.status_code == 201
    assert response.json() == sample_response.model_dump()


@pytest.mark.parametrize(
    "sample_id, sample_response",
    [
        (1, yeti_response),
        (2, bigfoot_response),
    ]
)
def test_get_by_id_success(
    sample_id: int,
    sample_response: CreatureResponse,
    public_client: TestClient,
):
    response = public_client.get(f"/creatures/{sample_id}")

    assert response.status_code == 200
    assert response.json() == sample_response.model_dump()


@pytest.mark.parametrize(
    "sample_id", [99]
)
def test_get_by_id_not_found(
    sample_id: int,
    public_client: TestClient,
):
    response = public_client.get(f"/creatures/{sample_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == f"Creature with ID {sample_id} not found"
