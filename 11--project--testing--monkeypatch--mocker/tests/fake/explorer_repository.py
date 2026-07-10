from app.models.explorers import ExplorerRequest, ExplorerResponse
from tests.fake.explorer_samples import hande_response, weiser_response


def _data() -> dict[int, ExplorerResponse]:
    return {
        1: hande_response,
        2: weiser_response,
    }


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
    return list(_data().values())


def get_by_id(explorer_id: int) -> ExplorerResponse | None:
    """Returns an explorer by its name"""
    try:
        return _data()[explorer_id]

    except IndexError:
        return None


def create(explorer: ExplorerRequest) -> ExplorerResponse:
    """Add an explorer"""
    data = _data()
    explorer_id = list(data.keys())[-1] + 1
    values = to_dict(explorer)
    values["id"] = explorer_id
    explorer = ExplorerResponse(**values)
    data[explorer_id] = explorer
    return explorer


# nonfunctional for now
def replace(explorer_id: int, explorer: ExplorerRequest) -> ExplorerResponse:
    """Completely replace an explorer"""
    raise NotImplementedError()


def delete(explorer_id: int) -> bool:
    """Delete an explorer; return `False` if it doesn't exist"""
    raise NotImplementedError()
