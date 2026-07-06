import pytest

from app.models.creatures import CreatureRequest, CreatureResponse
from app.services import creatures as service
from tests.unit.services import fake_creatures

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
    def setup_method(self):
        """Replace the original repository with the fake one before each test method."""
        self._original_repository = service.repository
        service.repository = fake_creatures

    def teardown_method(self):
        """Replace the fake repository with the original one after each test method."""
        service.repository = self._original_repository

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
        sample_response: CreatureResponse,
    ):
        result = service.create(sample_request)
        assert result == sample_response

    @pytest.mark.positive
    @pytest.mark.parametrize(
        "creature_id, expected",
        [
            (1, yeti_response),
            (2, bigfoot_response),
        ]
    )
    def test_get_by_id_positive(self, creature_id: int, expected: CreatureResponse):
        result = service.get_by_id(creature_id)
        assert result == expected

    @pytest.mark.negative
    @pytest.mark.parametrize(
        "creature_id",
        [999, 1000]
    )
    def test_get_by_id_negative(self, creature_id: int):
        result = service.get_by_id(creature_id)
        assert result is None
