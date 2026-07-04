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


def to_model(row: tuple) -> CreatureResponse:
    """Converts a tuple returned by a `fetch` function to a model object."""
    creature_id, name, country, area, description, aka = row
    return CreatureResponse(
        id=creature_id,
        name=name,
        country=country,
        area=area,
        description=description,
        aka=aka,
    )


def to_dict(creature: CreatureRequest) -> dict:
    """Converts a Pydantic model to a dictionary."""
    return creature.model_dump()


def get_all() -> list[CreatureResponse]:
    """Returns all creatures"""
    return _creatures


def get_one(creature_id: int) -> CreatureResponse | None:
    """Returns a creature by its name"""
    try:
        return _creatures[creature_id - 1]

    except IndexError:
        return None


def create(creature: CreatureRequest) -> CreatureResponse:
    """Add a creature"""
    creature_id = len(_creatures) + 1
    values = to_dict(creature)
    values["id"] = creature_id
    return CreatureResponse(**values)


# nonfunctional for now
def replace(creature_id: int, creature: CreatureRequest) -> CreatureResponse:
    """Completely replace a creature"""
    raise NotImplementedError()


def delete(creature_id: int) -> bool:
    """Delete an explorer; return `False` if it doesn't exist"""
    raise NotImplementedError()
