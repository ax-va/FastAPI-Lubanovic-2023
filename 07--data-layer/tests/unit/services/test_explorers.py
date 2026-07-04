import pytest

from app.models.explorers import ExplorerRequest, ExplorerResponse
from app.services import explorers as service
from tests.repositories import fake_explorers

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
        """Replace the original repository with the fake one before each test method."""
        self._original_repository = service.repository
        service.repository = fake_explorers

    def teardown_method(self):
        """Replace the fake repository with the original one after each test method."""
        service.repository = self._original_repository

    @pytest.mark.positive
    @pytest.mark.parametrize(
        "sample_request, sample_response",
        [
            (ax_va_request, ax_va_response)
        ]
    )
    def test_create(
        self,
        sample_request,
        sample_response,
    ):
        result = service.create(sample_request)
        assert result == sample_response

    @pytest.mark.positive
    @pytest.mark.parametrize(
        "explorer_id, expected",
        [
            (1, hande_response),
            (2, weiser_response),
        ]
    )
    def test_get_one_positive(self, explorer_id: int, expected: ExplorerResponse):
        result = service.get_one(explorer_id)
        assert result == expected

    @pytest.mark.negative
    @pytest.mark.parametrize(
        "explorer_id",
        [99, 100]
    )
    def test_get_one_negative(self, explorer_id):
        result = service.get_one(explorer_id)
        assert result is None
