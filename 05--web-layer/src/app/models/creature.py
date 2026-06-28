from pydantic import BaseModel


class Creature(BaseModel):
    id: int
    name: str
    country: str
    area: str
    description: str
    aka: str
