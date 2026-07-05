import sqlite3

import pytest

from app.models.creatures import CreatureRequest, CreatureResponse
from app.repositories.sqlite import database
from app.repositories.sqlite import creatures

repository = creatures

yeti_request = CreatureRequest(
    name="Yeti",
    country="CN",
    area="Himalayas",
    description="Hirsute Himalayan",
    aka="Abominable Snowman",
)
bigfoot_request = CreatureRequest(
    name="Bigfoot",
    description="Yeti's Cousin Eddie",
    country="US",
    area="*",
    aka="Sasquatch"
)
lubanovic_request = CreatureRequest(
    name="Lubanovic",
    country="US",
    area="*",
    description="Author",
    aka="*"
)

yeti_response = CreatureResponse(
    id=1,
    **yeti_request.model_dump(),
)
bigfoot_response = CreatureResponse(
    id=2,
    **bigfoot_request.model_dump(),
)
lubanovic_response = CreatureResponse(
    id=3,
    **lubanovic_request.model_dump(),
)


class Test:
    def setup_class(self):
        """Replace the original connection with the in-memory one before all test class methods."""
        self._original_conn = database.conn
        # Create a database in memory
        database.conn = sqlite3.connect(":memory:")
        # Initialize tables
        database.init()
        # Add initial rows
        repository.create(yeti_request)
        repository.create(bigfoot_request)

    def teardown_class(self):
        """Replace the in-memory connection with the original one after all test class methods."""
        database.conn = self._original_conn

    @pytest.mark.positive
    @pytest.mark.parametrize(
        "sample_request, sample_response",
        [
            (lubanovic_request, lubanovic_response),
        ]
    )
    def test_create(
        self,
        sample_request: CreatureRequest,
        sample_response: CreatureResponse
    ):
        result = repository.create(sample_request)
        assert result == sample_response

    @pytest.mark.positive
    @pytest.mark.parametrize(
        "creature_id, sample_response",
        [
            (1, yeti_response),
            (2, bigfoot_response),
        ]
    )
    def test_get_one_positive(self, creature_id: int, sample_response: CreatureResponse):
        result = repository.get_one(creature_id)
        assert result == sample_response

    @pytest.mark.negative
    @pytest.mark.parametrize(
        "creature_id",
        [999, 1000]
    )
    def test_get_one_negative(self, creature_id: int):
        result = repository.get_one(creature_id)
        assert result is None

    @pytest.mark.positive
    @pytest.mark.parametrize(
        "sample_request",
        [yeti_request, bigfoot_request]
    )
    def test_delete_positive(self, sample_request: CreatureRequest):
        creature = repository.create(sample_request)
        result = repository.delete(creature.id)
        assert result is True

    @pytest.mark.negative
    @pytest.mark.parametrize(
        "creature_id",
        [999, 1000]
    )
    def test_delete_negative(self, creature_id: int):
        result = repository.delete(creature_id)
        assert result is False
