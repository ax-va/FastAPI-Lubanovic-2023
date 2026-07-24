from pydantic import BaseModel


class ExplorerRequest(BaseModel):
    name: str
    country: str | None
    description: str | None


class ExplorerResponse(ExplorerRequest):
    id: int
