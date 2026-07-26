from sqlite3 import Connection
from typing import Generator

import pytest

from app.services import creatures as creatures_service
from app.services import explorers as explorers_service
from app.services import users as users_service
from app.repositories.sqlite import database as db
from tests.samples.creatures import yeti_request, bigfoot_request
from tests.samples.explorers import hande_request, weiser_request


@pytest.fixture
def db_connection() -> Generator[Connection, None, None]:
    with db.connect(":memory:") as connection:
        db.ensure_tables_exist(connection)
        users_service.create_admin(
            connection,
            username="admin",
            password="admin",
        )

        creatures_service.create(connection, yeti_request)
        creatures_service.create(connection, bigfoot_request)

        explorers_service.create(connection, hande_request)
        explorers_service.create(connection, weiser_request)

        yield connection
