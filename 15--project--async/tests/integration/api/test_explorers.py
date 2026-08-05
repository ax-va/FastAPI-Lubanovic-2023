import pytest
from httpx import AsyncClient

from app.models.schemas.explorers import ExplorerRequest, ExplorerResponse
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
async def test_create(
    sample_request: ExplorerRequest,
    sample_response: ExplorerResponse,
    user_client: AsyncClient,
) -> None:

    payload = sample_request.model_dump()

    # Authentication is bypassed by overriding `get_current_user`.
    # Requests don't require an Authorization header or JWT token.
    response = await user_client.post("/explorers", json=payload)

    assert response.status_code == 201
    assert response.json() == sample_response.model_dump()


@pytest.mark.positive
@pytest.mark.parametrize(
    "sample_response", [hande_response, weiser_response]
)
async def test_get_by_id_success(
    sample_response: ExplorerResponse,
    public_client: AsyncClient,
):
    response = await public_client.get(f"/explorers/{sample_response.id}")

    assert response.status_code == 200
    assert response.json() == sample_response.model_dump()


@pytest.mark.negative
@pytest.mark.parametrize(
    "sample_id", [99]
)
async def test_get_by_id_not_found(
    sample_id: int,
    public_client: AsyncClient,
):
    response = await public_client.get(f"/explorers/{sample_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == f"Explorer with ID {sample_id} not found"
