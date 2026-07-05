import sqlite3

import pytest

from app.models.explorers import ExplorerRequest, ExplorerResponse
from app.repositories.sqlite import database
from app.repositories.sqlite import explorers

repository = explorers

hande_request = ExplorerRequest(
    name="Claude Hande",
    country="FR",
    description="Scarce during full moons",
)
weiser_request = ExplorerRequest(
    name="Noah Weiser",
    country="DE",
    description="Myopic machete man",
)
ax_va_request = ExplorerRequest(
    name="AxVa",
    country="DE",
    description="Just a good man",
)

hande_response = ExplorerResponse(
    id=1,
    **hande_request.model_dump(),
)
weiser_response = ExplorerResponse(
    id=2,
    **weiser_request.model_dump(),
)
ax_va_response = ExplorerResponse(
    id=3,
    **ax_va_request.model_dump(),
)


class Test:
    def setup_method(self):
        """Replace the original connection with the in-memory one before all test class methods."""
        self._original_conn = database.conn
        # Create a database in memory
        database.conn = sqlite3.connect(":memory:")
        # Initialize tables
        database.init()
        # Add initial rows
        repository.create(hande_request)
        repository.create(weiser_request)

    def teardown_method(self):
        """Replace the in-memory connection with the original one after all test class methods."""
        database.conn = self._original_conn

    @pytest.mark.positive
    @pytest.mark.parametrize(
        "sample_request, sample_response",
        [
            (ax_va_request, ax_va_response)
        ]
    )
    def test_create(
        self,
        sample_request: ExplorerRequest,
        sample_response: ExplorerResponse,
    ):
        result = repository.create(sample_request)
        assert result == sample_response

    @pytest.mark.positive
    @pytest.mark.parametrize(
        "explorer_id, explorer_response",
        [
            (1, hande_response),
            (2, weiser_response),
        ]
    )
    def test_get_one_positive(self, explorer_id: int, explorer_response: ExplorerResponse):
        result = repository.get_one(explorer_id)
        assert result == explorer_response

    @pytest.mark.negative
    @pytest.mark.parametrize(
        "explorer_id",
        [999, 1000]
    )
    def test_get_one_negative(self, explorer_id: int):
        result = repository.get_one(explorer_id)
        assert result is None

    @pytest.mark.positive
    @pytest.mark.parametrize(
        "sample_request",
        [hande_request, weiser_request]
    )
    def test_delete_positive(self, sample_request: ExplorerRequest):
        explorer = repository.create(sample_request)
        result = repository.delete(explorer.id)
        assert result is True

    @pytest.mark.negative
    @pytest.mark.parametrize(
        "explorer_id",
        [999, 1000]
    )
    def test_delete_negative(self, explorer_id: int):
        result = repository.delete(explorer_id)
        assert result is False

