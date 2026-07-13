from sqlite3 import Connection

from fastapi.testclient import TestClient

from tests.samples.creature_samples import lubanovic_request


def test_create(
    creatures_sqlite_memory_db: Connection,
    user_client: TestClient,
) -> None:

    payload = lubanovic_request.model_dump()

    response = user_client.post("/creatures", json=payload)

    assert response.status_code == 201
    assert response.json() == {
        "id": 3,
        **payload,
    }
