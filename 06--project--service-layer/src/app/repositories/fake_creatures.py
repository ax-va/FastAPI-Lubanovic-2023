from app.models.creatures import CreatureRequest, CreatureResponse

# stubs, or fake data
_creatures: list[CreatureResponse] = [
    CreatureResponse(
        id=1,
        name="Yeti",
        aka="Abominable Snowman",
        country="CN",
        area="Himalayas",
        description="Hirsute Himalayan",
    ),
    CreatureResponse(
        id=2,
        name="Bigfoot",
        description="Yeti's Cousin Eddie",
        country="US",
        area="*",
        aka="Sasquatch"
    ),
]


def get_all() -> list[CreatureResponse]:
    """Returns all creatures"""
    return _creatures


def get_by_id(creature_id: int) -> CreatureResponse | None:
    """Returns a creature by its name"""
    try:
        return _creatures[creature_id - 1]

    except IndexError:
        return None


# nonfunctional for now
def create(creature: CreatureRequest) -> CreatureResponse:
    """Add a creature"""
    raise NotImplementedError()


def replace(creature_id: int, creature: CreatureRequest) -> CreatureResponse:
    """Completely replace a creature"""
    raise NotImplementedError()


def delete(creature_id: int) -> bool:
    """Delete an explorer; return `False` if it doesn't exist"""
    raise NotImplementedError()
