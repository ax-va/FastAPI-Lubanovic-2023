import pytest
from app.models.creature import Creature
from app.repositories import fake_creatures
from app.services import creatures as code

yeti = Creature(
    name="Yeti",
    country="CN",
    area="Himalayas",
    description="Hirsute Himalayan",
    aka="Abominable Snowman",
)
bigfoot = Creature(
    name="Bigfoot",
    description="Yeti's Cousin Eddie",
    country="US",
    area="*",
    aka="Sasquatch"
)


class Test:
    def setup_method(self):
        """Replace the original repository with the fake one before each test method."""
        self._original_repository = code.repository
        code.repository = fake_creatures

    def teardown_method(self):
        """Replace the fake repository with the original one after each test method."""
        code.repository = self._original_repository

    @pytest.mark.parametrize(
        "sample",
        [yeti, bigfoot]
    )
    def test_create(self, sample: Creature):
        result = code.create(sample)
        assert result == sample

    @pytest.mark.positive
    @pytest.mark.parametrize(
        "creature_id, expected",
        [
            (1, yeti),
            (2, bigfoot),
        ]
    )
    def test_get_one_positive(self, creature_id: int, expected: Creature):
        result = code.get_one(creature_id)
        assert result == expected

    @pytest.mark.negative
    @pytest.mark.parametrize(
        "creature_id",
        [999, 1000]
    )
    def test_get_one_negative(self, creature_id):
        result = code.get_one(creature_id)
        assert result is None
