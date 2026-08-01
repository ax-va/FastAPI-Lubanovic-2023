from collections.abc import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool.impl import StaticPool

# Import all ORM models to create tables by `create_all` later
import app.models.orm  # noqa: F401
from app.models.orm.base import Base
from app.services import creatures as creatures_service
from app.services import explorers as explorers_service
from app.services import users as users_service
from tests.samples.creatures import yeti_request, bigfoot_request
from tests.samples.explorers import hande_request, weiser_request


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        # Reuse a single connection
        # so all sessions share the same in-memory database.
        poolclass=StaticPool,
    )

    Base.metadata.create_all(engine)

    session_factory = sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )

    with session_factory() as session:
        users_service.create_admin(
            session,
            username="admin",
            password="admin",
        )

        creatures_service.create(session, yeti_request)
        creatures_service.create(session, bigfoot_request)

        explorers_service.create(session, hande_request)
        explorers_service.create(session, weiser_request)

        yield session

    # Release all engine resources
    engine.dispose()
