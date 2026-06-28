from app.models.explorer import Explorer

# stubs, or fake data
_explorers: dict[int, Explorer] = {
    1: Explorer(
        id=1,
        name="Claude Hande",
        country="FR",
        description="Scarce during full moons",
    ),
    2: Explorer(
        id=2,
        name="Noah Weiser",
        country="DE",
        description="Myopic machete man",
    ),
}


def get_all() -> list[Explorer]:
    """Returns all explorers"""
    return list(_explorers.values())


def get_one(explorer_id: int) -> Explorer | None:
    """Returns an explorer by its name"""
    return _explorers.get(explorer_id)


# nonfunctional for now
def create(explorer: Explorer) -> Explorer:
    """Add an explorer"""
    return explorer


def replace(explorer: Explorer) -> Explorer:
    """Completely replace an explorer"""
    return explorer


def modify(explorer: Explorer) -> Explorer:
    """Partially modify an explorer"""
    return explorer


def delete(explorer_id: int) -> bool:
    """Delete an explorer; return `False` if it doesn't exist"""
    return False
