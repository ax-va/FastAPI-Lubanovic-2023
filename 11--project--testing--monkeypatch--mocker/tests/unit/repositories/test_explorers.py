import sqlite3
from sqlite3 import Connection
from typing import Generator

import pytest

from app.models.explorers import ExplorerRequest, ExplorerResponse
from app.repositories.sqlite import explorers as repository
from app.repositories.sqlite import database as db
from tests.fake.explorer_samples import (
    hande_request,
    hande_response,
    weiser_request,
    weiser_response,
    ax_va_request,
    ax_va_response,
)


@pytest.fixture
def sqlite_memory_db(monkeypatch) -> Generator[Connection, None, None]:
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row

    # Monkeypatch replaces a real object with another real object.
    # Use it when the code should continue working normally,
    # but with a different implementation,
    # e.g., an in-memory SQLite database.
    monkeypatch.setattr(db, "conn", connection)

    connection.execute(
        "CREATE TABLE IF NOT EXISTS explorers ("
        "   id INTEGER PRIMARY KEY, "
        "   name TEXT NOT NULL, "
        "   country TEXT, "
        "   description TEXT"
        ")"
    )

    insert_query = (
        "INSERT INTO explorers (name, country, description) "
        "VALUES (:name, :country, :description)"
    )
    for sample_request in [hande_request, weiser_request]:
        connection.execute(insert_query, sample_request.model_dump())

    connection.commit()

    yield connection

    connection.close()


@pytest.mark.parametrize(
    "sample_request, sample_response",
    [
        (ax_va_request, ax_va_response),
    ]
)
def test_create(
        sample_request: ExplorerRequest,
        sample_response: ExplorerResponse,
        sqlite_memory_db: Connection,
):
    missing = repository.get_by_id(sample_response.id)
    assert missing is None

    num_rows_before = len(repository.get_all())
    assert num_rows_before == 2

    created = repository.create(sample_request)
    assert created == sample_response

    num_rows_after = len(repository.get_all())
    assert num_rows_after == num_rows_before + 1

    stored = repository.get_by_id(sample_response.id)
    assert stored == sample_response

    hande_available = repository.get_by_id(1)
    assert hande_available == hande_response

    weiser_available = repository.get_by_id(2)
    assert weiser_available == weiser_response


@pytest.mark.positive
@pytest.mark.parametrize(
    "sample_id, sample_response",
    [
        (1, hande_response),
        (2, weiser_response),
        (3, None),
    ]
)
def test_get_by_id(
        sample_id: int,
        sample_response: ExplorerResponse,
        sqlite_memory_db: Connection,
):
    got = repository.get_by_id(sample_id)
    assert got == sample_response


@pytest.mark.positive
@pytest.mark.parametrize(
    "sample_id, expected",
    [
        (1, True),
        (2, True),
        (3, False),

    ]
)
def test_delete(
        sample_id: int,
        expected: bool,
        sqlite_memory_db: Connection,
):
    num_rows_before = len(repository.get_all())
    assert num_rows_before == 2

    deleted = repository.delete(sample_id)
    assert deleted is expected

    num_rows_after = len(repository.get_all())
    if expected:
        assert num_rows_after == num_rows_before - 1
    else:
        assert num_rows_after == num_rows_before

    missing = repository.get_by_id(sample_id)
    assert missing is None
