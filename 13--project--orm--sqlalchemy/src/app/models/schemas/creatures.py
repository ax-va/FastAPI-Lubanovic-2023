from pydantic import BaseModel


class CreatureRequest(BaseModel):
    name: str
    country: str | None = None
    area: str | None = None
    description: str | None = None
    aka: str | None = None


class CreatureResponse(CreatureRequest):
    id: int
