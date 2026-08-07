from pydantic import BaseModel


class CreatureRequest(BaseModel):
    name: str
    country: str | None
    area: str | None
    description: str | None
    aka: str | None


class CreatureResponse(CreatureRequest):
    id: int
