import sqlite3
from sqlite3 import Connection
from typing import Generator

import pytest

from app.repositories.sqlite import database as db
from tests.samples.creatures import yeti_request, bigfoot_request
from tests.samples.explorers import hande_request, weiser_request


@pytest.fixture
def sqlite_conn(monkeypatch: pytest.MonkeyPatch) -> Generator[Connection, None, None]:
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row

    yield conn

    conn.close()


@pytest.fixture
def creatures_sqlite_db(
    sqlite_conn: Connection,
    monkeypatch: pytest.MonkeyPatch,
) -> Connection:
    # Monkeypatch replaces a real object with another real object.
    # Use it when the code should continue working normally,
    # but with a different implementation,
    # e.g., an in-memory SQLite database.
    monkeypatch.setattr(db, "conn", sqlite_conn)

    sqlite_conn.execute(
        "CREATE TABLE creatures ("
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
        sqlite_conn.execute(insert_query, sample_request.model_dump())

    sqlite_conn.commit()

    return sqlite_conn


@pytest.fixture
def explorers_sqlite_db(
    sqlite_conn: Connection,
    monkeypatch: pytest.MonkeyPatch,
) -> Connection:
    # Monkeypatch replaces a real object with another real object.
    # Use it when the code should continue working normally,
    # but with a different implementation,
    # e.g., an in-memory SQLite database.
    monkeypatch.setattr(db, "conn", sqlite_conn)

    sqlite_conn.execute(
        "CREATE TABLE explorers ("
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
        sqlite_conn.execute(insert_query, sample_request.model_dump())

    sqlite_conn.commit()

    return sqlite_conn
