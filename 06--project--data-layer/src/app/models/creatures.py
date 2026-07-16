from pydantic import BaseModel


class CreatureRequest(BaseModel):
    name: str
    country: str
    area: str
    description: str
    aka: str


class CreatureResponse(CreatureRequest):
    id: int
