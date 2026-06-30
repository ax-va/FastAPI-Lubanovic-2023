import pytest
from app.models.explorer import Explorer
from app.repositories import fake_explorers
from app.services import explorers as code

hande = Explorer(
    id=1,
    name="Claude Hande",
    country="FR",
    description="Scarce during full moons",
)
weiser = Explorer(
    id=2,
    name="Noah Weiser",
    country="DE",
    description="Myopic machete man",
)


class Test:
    def setup_method(self):
        """Replace the original repository with the fake one before each test method."""
        self._original_repository = code.repository
        code.repository = fake_explorers

    def teardown_method(self):
        """Replace the fake repository with the original one after each test method."""
        code.repository = self._original_repository

    @pytest.mark.positive
    @pytest.mark.parametrize(
        "sample",
        [hande, weiser]
    )
    def test_create(self, sample: Explorer):
        result = code.create(sample)
        assert result == sample

    @pytest.mark.positive
    @pytest.mark.parametrize(
        "explorer_id, expected",
        [
            (1, hande),
            (2, weiser),
        ]
    )
    def test_get_one_positive(self, explorer_id: int, expected: Explorer):
        result = code.get_one(explorer_id)
        assert result == expected

    @pytest.mark.negative
    @pytest.mark.parametrize(
        "explorer_id",
        [99, 100]
    )
    def test_get_one_negative(self, explorer_id):
        result = code.get_one(explorer_id)
        assert result is  None
