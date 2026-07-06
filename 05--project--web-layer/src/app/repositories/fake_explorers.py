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


def get_all() -> list[ExplorerResponse]:
    """Returns all explorers"""
    return _explorers


def get_by_id(explorer_id: int) -> ExplorerResponse | None:
    """Returns an explorer by its name"""
    try:
        return _explorers[explorer_id - 1]

    except IndexError:
        return None


# nonfunctional for now
def create(explorer: ExplorerRequest) -> ExplorerResponse:
    """Add an explorer"""
    raise NotImplementedError()


def replace(explorer_id: int, explorer: ExplorerRequest) -> ExplorerResponse:
    """Completely replace an explorer"""
    raise NotImplementedError()


def delete(explorer_id: int) -> bool:
    """Delete an explorer; return `False` if it doesn't exist"""
    raise NotImplementedError()
