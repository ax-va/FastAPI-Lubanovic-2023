from app.models.creature import Creature
from app.repositories import fake_creatures
from app.service import creatures as code

sample = Creature(
    name="yeti",
    country="CN",
    area="Himalayas",
    description="Hirsute Himalayan",
    aka="Abominable Snowman",
)


class Test:
    def setup_method(self):
        self.initial_repo = code.repository
        code.repository = fake_creatures

    def teardown_method(self):
        code.repository = self.initial_repo

    def test_create(self):
        result = code.create(sample)
        assert result == sample

    def test_get_one_positive(self):
        result = code.get_one(1)
        assert result == sample

    def test_get_one_negative(self):
        result = code.get_one(1000)
        assert result is None
