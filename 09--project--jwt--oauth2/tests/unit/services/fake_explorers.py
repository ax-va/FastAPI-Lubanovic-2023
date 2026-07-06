from app.models.explorers import ExplorerRequest, ExplorerResponse

# stubs, or fake data
_explorers: list[ExplorerResponse] = [
    ExplorerResponse(
        id=1,
        name="Claude Hande",
        country="FR",
        description="Scarce during full moons",
    ),
    ExplorerResponse(
        id=2,
        name="Noah Weiser",
        country="DE",
        description="Myopic machete man",
    ),
]


def to_model(row: tuple) -> ExplorerResponse:
    """Converts a tuple returned by a `fetch` function to a model object."""
    explorer_id, name, country, description = row
    return ExplorerResponse(
        id=explorer_id,
        name=name,
        country=country,
        description=description,
    )


def to_dict(explorer: ExplorerRequest) -> dict:
    """Converts a Pydantic model to a dictionary."""
    return explorer.model_dump()


def get_all() -> list[ExplorerResponse]:
    """Returns all explorers"""
    return _explorers


def get_by_id(explorer_id: int) -> ExplorerResponse | None:
    """Returns an explorer by its name"""
    try:
        return _explorers[explorer_id - 1]

    except IndexError:
        return None


def create(explorer: ExplorerRequest) -> ExplorerResponse:
    """Add an explorer"""
    explorer_id = len(_explorers) + 1
    values = to_dict(explorer)
    values["id"] = explorer_id
    return ExplorerResponse(**values)


# nonfunctional for now
def replace(explorer_id: int, explorer: ExplorerRequest) -> ExplorerResponse:
    """Completely replace an explorer"""
    raise NotImplementedError()


def delete(explorer_id: int) -> bool:
    """Delete an explorer; return `False` if it doesn't exist"""
    raise NotImplementedError()
