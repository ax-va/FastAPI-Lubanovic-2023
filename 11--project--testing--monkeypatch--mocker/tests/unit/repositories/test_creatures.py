import sqlite3
from sqlite3 import Connection
from typing import Generator

import pytest

from app.models.creatures import CreatureRequest, CreatureResponse
from app.repositories.sqlite import creatures as repository
from app.repositories.sqlite import database as db
from tests.fake.creature_samples import (
    yeti_request,
    yeti_response,
    bigfoot_request,
    bigfoot_response,
    lubanovic_request,
    lubanovic_response,
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
        "CREATE TABLE IF NOT EXISTS creatures ("
        "   id INTEGER PRIMARY KEY, "
        "   name TEXT NOT NULL, "
        "   country TEXT, "
        "   area TEXT, "
        "   description TEXT, "
        "   aka TEXT"
        ")"
    )

    insert_query = (
        "INSERT INTO creatures (name, country, area, description, aka) "
        "VALUES (:name, :country, :area, :description, :aka)"
    )
    for sample_request in [yeti_request, bigfoot_request]:
        connection.execute(insert_query, sample_request.model_dump())

    connection.commit()

    yield connection

    connection.close()


class Test:
    @pytest.mark.parametrize(
        "sample_request, sample_response",
        [
            (lubanovic_request, lubanovic_response),
        ]
    )
    def test_create(
        self,
        sample_request: CreatureRequest,
        sample_response: CreatureResponse,
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

        yeti_available = repository.get_by_id(1)
        assert yeti_available == yeti_response

        bigfoot_available = repository.get_by_id(2)
        assert bigfoot_available == bigfoot_response

    @pytest.mark.positive
    @pytest.mark.parametrize(
        "sample_id, sample_response",
        [
            (1, yeti_response),
            (2, bigfoot_response),
            (3, None),
        ]
    )
    def test_get_by_id(
        self,
        sample_id: int,
        sample_response: CreatureResponse,
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
        self,
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
