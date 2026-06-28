from app.models.creature import Creature


# stubs, or fake data
_creatures: dict[int, Creature] = {
    1: Creature(
        id=1,
        name="Yeti",
        aka="Abominable Snowman",
        country="CN",
        area="Himalayas",
        description="Hirsute Himalayan",
    ),
    2: Creature(
        id=2,
        name="Bigfoot",
        description="Yeti's Cousin Eddie",
        country="US",
        area="*",
        aka="Sasquatch"
    ),
}


def get_all() -> list[Creature]:
    """Returns all creatures"""
    return list(_creatures.values())


def get_one(creature_id: int) -> Creature | None:
    """Returns a creature by its name"""
    return _creatures.get(creature_id)


# nonfunctional for now
def create(creature: Creature) -> Creature:
    """Add a creature"""
    return creature


def replace(creature: Creature) -> Creature:
    """Completely replace a creature"""
    return creature


def modify(creature: Creature) -> Creature:
    """Partially modify a creature"""
    return creature


def delete(creature_id: int) -> bool:
    """Delete an explorer; return `False` if it doesn't exist"""
    return False
