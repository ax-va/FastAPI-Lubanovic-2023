from pydantic import BaseModel


class ExplorerRequest(BaseModel):
    name: str
    country: str | None = None
    description: str | None = None


class ExplorerResponse(ExplorerRequest):
    id: int
