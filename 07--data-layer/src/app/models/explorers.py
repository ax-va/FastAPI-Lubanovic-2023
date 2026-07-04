from pydantic import BaseModel


class ExplorerRequest(BaseModel):
    name: str
    country: str
    description: str


class ExplorerResponse(ExplorerRequest):
    id: int
